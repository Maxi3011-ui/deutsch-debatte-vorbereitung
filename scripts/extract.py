"""Import the supplied, finished preparation PDF without summarizing its content."""
import json, re, subprocess, sys
from speeches import apply_speeches
from pathlib import Path
root = Path(__file__).resolve().parents[1]
source = Path(sys.argv[1]) if len(sys.argv)>1 else Path.home()/'Downloads/Debatte_Pruefungsmappe_Neu_nach_Rollen.pdf'
raw = subprocess.check_output(['pdftotext','-layout',str(source),'-'], text=True)
headings = {'Deine spezielle Aufgabe','Deine drei Hauptargumente','Vorschlag und kritische Punkte','Eröffnungsrede – dein konkretes Gerüst','Wahrscheinliche Angriffe – schnell reagieren','Was die Gegenseite wahrscheinlich sagt','Deine zwei guten Rückfragen','Schlussrede – erst nach der Debatte anpassen','Deine Notizvorlage in der Vorbereitungszeit','Bewertung: Vier Dinge zählen','Eröffnung – 2 Minuten pro Person','Freie Aussprache – 8 Minuten insgesamt','Schlussrede – 1 Minute pro Person','Wenn du kurz hängen bleibst','Argumente','Fair widersprechen','Gegenfragen','Abwägen','Fakten und sprachliche Fallen'}
argument_titles = {'Sicherheit','Arbeitsmarkt','Demokratie','Medizin und Forschung','Internationaler Wettbewerb','Regulierung statt Bremse','Historische Benachteiligung','Vielfalt und Identifikation','Kanon weiterentwickeln','Literarische Qualität','Historisches Verständnis','Ergänzen statt Ersetzen'}
pages=[]
for number, page in enumerate(raw.split('\f'),1):
    if not page.strip(): continue
    clean = re.sub(r'^Deutsch-Debatte · Prüfungsmappe\s+Seite \d+\s*$', '', page, flags=re.M).strip()
    lines=clean.splitlines(); title=lines.pop(0).strip()
    if lines and lines[0].strip()=='NUR DIESES ROLLENPAKET + ALLGEMEINES BENUTZEN': lines.pop(0)
    blocks=[]
    for paragraph in re.split(r'\n\s*\n', '\n'.join(lines).strip()):
        pending=[]
        def flush():
            if pending:
                text=' '.join(pending)
                blocks.append({'kind':'li' if text.startswith('• ') else 'p','text':text.removeprefix('• ')})
                pending.clear()
        for line in paragraph.splitlines():
            line=line.strip()
            if line in headings or line in argument_titles:
                flush(); blocks.append({'kind':'h3' if line in headings else 'h4','text':line})
            else: pending.append(line)
        flush()
    pages.append({'number':number,'title':title,'blocks':blocks})
assert len(pages)==20
roles=['pro1','pro2','contra1','contra2']
topics=[{'id':'ki','label':'KI-Entwicklung','question':'Soll die Entwicklung besonders leistungsfähiger KI-Systeme bewusst verlangsamt werden, bis ihre gesellschaftlichen Folgen besser abgeschätzt werden können?','clarification':'KI = verlangsamen, nicht verbieten.'},{'id':'literatur','label':'Schullektüren','question':'Soll bei der Auswahl von Schullektüren stärker darauf geachtet werden, dass Werke von Schriftstellerinnen angemessen vertreten sind, auch wenn dafür Werke des traditionellen literarischen Kanons entfallen?','clarification':'Literatur = einzelne Werke ersetzen können, nicht alle Klassiker abschaffen.'}]
for t,offset in zip(topics,[4,12]):
    t['roles']={role:{'label':label,'pages':pages[offset+i*2:offset+i*2+2]} for i,(role,label) in enumerate(zip(roles,['Pro 1','Pro 2','Contra 1','Contra 2']))}
    for role in t['roles'].values():
        assert sum(b['kind']=='h4' for p in role['pages'] for b in p['blocks'])==3
        assert len(role['pages'])==2
payload={'source':source.name,'topics':topics,'general':pages[1:4]}
payload = apply_speeches(payload)
(root/'tmp').mkdir(exist_ok=True)
(root/'content.js').write_text('window.DEBATE = '+json.dumps(payload,ensure_ascii=False,indent=2)+';\n')
(root/'tmp/source.txt').write_text(raw)
print('Imported 2 topics, 8 complete two-page role packages, 3 general pages.')
