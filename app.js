(() => {
  'use strict';
  const data = window.DEBATE;
  if (!data) return;
  const $ = id => document.getElementById(id);
  const topicSelect = $('topic'), roleSelect = $('role');
  const storage = {
    get(key) { try { return localStorage.getItem(key); } catch { return null; } },
    set(key, value) { try { localStorage.setItem(key, value); } catch { /* Reading also works with storage disabled. */ } }
  };
  const params = new URLSearchParams(location.search);
  const validTopic = id => data.topics.some(t => t.id === id);
  const validRole = id => Object.hasOwn(data.topics[0].roles, id);
  const initialTopic = params.get('thema') || storage.get('debate-topic');
  const initialRole = params.get('rolle') || storage.get('debate-role');
  topicSelect.value = validTopic(initialTopic) ? initialTopic : 'ki';
  roleSelect.value = validRole(initialRole) ? initialRole : 'pro1';
  const esc = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const labels = ['Annahme:', 'Deine Position:', 'Kernaussage:', 'Beleg / Beispiel:', 'Bezug zur Streitfrage:', 'Möglicher Einwand:', 'Antwort:', 'Möglicher Pro-1-Vorschlag:', 'Prüffragen / Schwachstellen:', 'Zusätzlicher Gedanke:', 'Vor der Debatte merken:', 'Hinweis:', 'Letzte Regel:'];
  function format(text) {
    const label = labels.find(l => text.startsWith(l));
    if (label) return '<strong>' + esc(label) + '</strong> ' + esc(text.slice(label.length).trim());
    // Keep fill-in lines inside narrow watch screens without a long underline overflowing.
    return esc(text).replace(/_{4,}/g, '…');
  }
  function renderPage(page, scope) {
    let html = '<section class="page" data-source-page="' + page.number + '"><p class="page-label">' + esc(scope === 'role' ? (page.updatedOpening ? 'Redeplan · mit deiner Eröffnungsrede' : 'Dein Rollenpaket · PDF ' + page.number) : page.title.replace(/^ALLGEMEINES \d \| /, '')) + '</p>';
    let inList = false;
    page.blocks.forEach(block => {
      if (inList && block.kind !== 'li') { html += '</ul>'; inList = false; }
      if (block.kind === 'li' && !inList) { html += '<ul>'; inList = true; }
      const tag = block.kind;
      let id = '';
      if (scope === 'role' && block.text === 'Deine drei Hauptargumente') id = ' id="arguments"';
      if (scope === 'role' && block.anchor === 'opening') id = ' id="opening"';
      const cls = block.annotation ? ' class="note"' : block.speech ? ' class="speech-text"' : block.text.startsWith('Deine Position:') ? ' class="lead"' : block.text.startsWith('Antwort:') ? ' class="answer"' : /^(Vor der Debatte merken:|Hinweis:|Letzte Regel:)/.test(block.text) ? ' class="note"' : '';
      html += '<' + tag + id + cls + '>' + format(block.text) + '</' + tag + '>';
    });
    return html + (inList ? '</ul>' : '') + '</section>';
  }
  function render() {
    const topic = data.topics.find(t => t.id === topicSelect.value);
    const role = topic.roles[roleSelect.value];
    $('selection-status').textContent = topic.label + ' · ' + role.label;
    $('question-title').textContent = topic.question;
    $('clarification').textContent = topic.clarification;
    $('role-content').innerHTML = role.pages.map(p => renderPage(p, 'role')).join('');
    $('role-content').setAttribute('aria-label', topic.label + ' · ' + role.label);
    document.title = topic.label + ' · ' + role.label + ' | Deutsch-Debatte';
    storage.set('debate-topic', topic.id);
    storage.set('debate-role', roleSelect.value);
    const url = new URL(location.href);
    url.searchParams.set('thema', topic.id);
    url.searchParams.set('rolle', roleSelect.value);
    try { history.replaceState(null, '', url); } catch { /* Also usable as a local file. */ }
  }
  $('general-content').innerHTML = data.general.map(p => renderPage(p, 'general')).join('');
  topicSelect.addEventListener('change', render);
  roleSelect.addEventListener('change', render);
  document.querySelectorAll('[data-jump]').forEach(button => button.addEventListener('click', () => {
    if (button.dataset.jump === 'top') window.scrollTo(0, 0);
    else $(button.dataset.jump)?.scrollIntoView({block:'start'});
  }));
  let scale = Number(storage.get('debate-font')) || 1;
  const min = .9, max = 1.4;
  function setScale(next) {
    scale = Math.max(min, Math.min(max, Math.round(next * 10) / 10));
    document.documentElement.style.setProperty('--text-scale', scale);
    $('type-status').textContent = Math.round(scale * 100) + ' %';
    $('smaller').disabled = scale <= min;
    $('larger').disabled = scale >= max;
    storage.set('debate-font', String(scale));
  }
  $('smaller').addEventListener('click', () => setScale(scale - .1));
  $('larger').addEventListener('click', () => setScale(scale + .1));
  window.addEventListener('popstate', () => {
    const current = new URLSearchParams(location.search);
    if (validTopic(current.get('thema'))) topicSelect.value = current.get('thema');
    if (validRole(current.get('rolle'))) roleSelect.value = current.get('rolle');
    render();
  });
  setScale(scale);
  render();
})();
