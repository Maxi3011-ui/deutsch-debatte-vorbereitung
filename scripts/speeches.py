"""Apply the user's complete opening speeches after importing the source PDF."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADING = 'Eröffnungsrede – ausformuliert'
ADAPTATION = 'Hinweis: Bei Contra 1, Pro 2 und Contra 2 ist die ausformulierte Rede dein Ausgangspunkt. Passe sie an das an, was deine Vorredner tatsächlich gesagt haben.'


def apply_speeches(payload):
    parts = re.split(r'^## (ki|literatur)/(pro1|pro2|contra1|contra2)\s*$', (ROOT / 'eroeffnungsreden.md').read_text(), flags=re.M)
    speeches = {}
    for i in range(1, len(parts), 3):
        topic, role, text = parts[i:i + 3]
        sections = {'Rede': []}
        current = 'Rede'
        for paragraph in re.split(r'\n\s*\n', text.strip()):
            if paragraph.startswith('### '):
                current = paragraph[4:].strip()
                sections.setdefault(current, [])
            else:
                sections[current].append(paragraph.strip())
        speeches[(topic, role)] = sections
    if len(speeches) != 8:
        raise ValueError('Expected exactly eight opening speeches')
    for topic in payload['topics']:
        for role_id, role in topic['roles'].items():
            speech = speeches[(topic['id'], role_id)]
            page = role['pages'][1]
            blocks = page['blocks']
            start = next(i for i, b in enumerate(blocks) if b['kind'] == 'h3' and b['text'].startswith('Eröffnungsrede –'))
            end = next(i for i in range(start + 1, len(blocks)) if blocks[i]['kind'] == 'h3')
            replacement = [{'kind': 'h3', 'text': HEADING, 'anchor': 'opening'}]
            for paragraph in speech.get('Annahme', []):
                replacement.append({'kind': 'p', 'text': 'Annahme: ' + paragraph, 'annotation': True})
            if role_id != 'pro1':
                replacement.append({'kind': 'p', 'text': ADAPTATION, 'annotation': True})
            replacement.extend({'kind': 'p', 'text': p, 'speech': True} for p in speech['Rede'])
            replacement.extend({'kind': 'p', 'text': 'Hinweis: ' + p, 'annotation': True} for p in speech.get('Hinweis', []))
            page['blocks'] = blocks[:start] + replacement + blocks[end:]
            page['updatedOpening'] = True
    # Use the user's updated plan in place of the original six time slots.
    plan = payload['general'][0]['blocks']
    end = next(i for i, b in enumerate(plan) if b['kind'] == 'h3')
    schedule = [
        '0–3 Minuten: Deine zugeloste Rede aufschlagen und vollständig lesen.',
        '3–10 Minuten: Rede an deine Rolle und den konkreten Vorschlag anpassen.',
        '10–17 Minuten: Eröffnungsrede zwei- bis dreimal laut durchsprechen.',
        '17–23 Minuten: Die drei wichtigsten Argumente und Gegenargumente einprägen.',
        '23–27 Minuten: Schlussrede und mögliche Reaktionen vorbereiten.',
        '27–30 Minuten: Eröffnungsrede ein letztes Mal frei sprechen.',
    ]
    payload['general'][0]['blocks'] = ([{'kind': 'p', 'text': p} for p in schedule]
        + [{'kind': 'p', 'text': 'Hinweis: Nutze die 30 Minuten nicht dazu, eine Rede Wort für Wort auswendig zu lernen.'},
           {'kind': 'p', 'text': ADAPTATION},
           {'kind': 'p', 'text': 'Hinweis: Klare Aussagen, konkrete Beispiele und direkte Reaktionen auf die Gegenseite sind überzeugender als möglichst viele Fremdwörter.'}]
        + plan[end:])
    payload['general'][0]['updatedPreparation'] = True
    return payload


if __name__ == '__main__':
    target = ROOT / 'content.js'
    payload = json.loads(target.read_text().removeprefix('window.DEBATE = ').removesuffix(';\n'))
    target.write_text('window.DEBATE = ' + json.dumps(apply_speeches(payload), ensure_ascii=False, indent=2) + ';\n')
    print('Applied eight complete opening speeches and the updated preparation schedule.')
