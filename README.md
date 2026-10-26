# Deutsch · Debattenvorbereitung

Apple-Watch-optimierte Website aus `Debatte_Pruefungsmappe_Neu_nach_Rollen.pdf`.

Oben Thema und Position wählen. Angezeigt wird ausschließlich das gewählte vollständige Rollenpaket (je zwei PDF-Seiten), darunter der allgemeine Teil (PDF-Seiten 2–4). Zwei Themen: KI-Entwicklung und Schullektüren. Vier Positionen pro Thema: Pro 1, Pro 2, Contra 1, Contra 2. Die ursprünglichen Redepläne wurden durch die acht vom Nutzer bereitgestellten vollständigen Eröffnungsreden ersetzt. Annahmen und Anpassungshinweise stehen außerhalb des gesprochenen Redetextes. Der allgemeine Teil verwendet den neuen 30-Minuten-Vorbereitungsplan. Die übrigen Inhalte aus der PDF bleiben erhalten. Die Anleitung der Titelseite wird durch die Auswahloberfläche ersetzt; die jeweiligen Streitfragen und die Abgrenzung werden angezeigt. Ausfülllinien der Notizvorlage erscheinen als Auslassungspunkte.

Auswahl und Schriftgröße werden lokal gespeichert. Direkte Links: `?thema=ki&rolle=pro1` bzw. `?thema=literatur&rolle=contra2`. URL-Auswahl hat Vorrang vor gespeichertem Zustand. Alle allgemeinen Hinweise bleiben unter dem Rollenpaket lesbar.

Keine externen Schriften, Bibliotheken, Tracker oder Netzwerkabhängigkeiten. Dunkle Watch-Ansicht bis 280 CSS-Pixel, größenverstellbarer Text und 44-Pixel-Bedienelemente. Keine fixierten Leisten. Außerhalb des schmalen Layouts warme Papieransicht. Browser-Druck enthält nur die ausgewählte Rolle plus Allgemeines.

## Lokal öffnen

`index.html` direkt öffnen oder `python3 -m http.server 8765` im Projektordner starten.

## Quelle neu importieren

`python3 scripts/extract.py /absoluter/pfad/zur/Debatte_Pruefungsmappe_Neu_nach_Rollen.pdf`

Benötigt `pdftotext` (Poppler). `content.js` enthält die importierten Absätze und die übernommenen Reden. `eroeffnungsreden.md` ist die Textquelle für alle acht Reden; `scripts/speeches.py` setzt sie nach dem PDF-Import ein. Die angepassten Redeplanseiten sind in der Oberfläche als solche gekennzeichnet. Die Original-PDF wird nicht mitveröffentlicht.
