"""Regenerate static content from supplied materials. Requires Python and Pillow.
Cloudflare deploys the committed public directory using the dependency-free Node build.
"""
from pathlib import Path
from PIL import Image
from html import escape
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import shutil
import json

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
ASSETS = PUBLIC / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)
SOURCE = ROOT / 'podklady'

def optimize(source, name, width):
    with Image.open(source) as image:
        image.thumbnail((width, width * 3), Image.Resampling.LANCZOS)
        image.save(ASSETS / name, 'WEBP', quality=86, method=6)
    return name

optimize(SOURCE / 'Logo.png', 'logo.webp', 700)
optimize(SOURCE / 'Pozvánka.png', 'pozvanka.webp', 1200)
optimize(SOURCE / 'Úvodní slovo.png', 'uvodni-slovo.webp', 1400)
shutil.copy2(SOURCE / 'Tršicko_program_A2.pdf', ASSETS / 'program-2026-2030.pdf')
shutil.copy2(SOURCE / 'Plakat_hlavy-1.pdf', ASSETS / 'kandidatka.pdf')

program = [
('Správa obcí a transparentnost', [
'Chceme jasnou, otevřenou a srozumitelnou komunikaci mezi vedením obce a občany.',
'Zaměříme se na moderní a efektivní fungování obecního úřadu.',
'Podpoříme zapojení obyvatel do rozhodovacího procesu.',
'Budeme pravidelně pořádat veřejná setkání s občany i mimo veřejná zastupitelstva.']),
('Rozvoj infrastruktury v jednotlivých obcích', [
'Budeme pečovat o obecní majetek a veřejná prostranství.',
'Připravíme jasnou koncepci využití obecních budov a pozemků včetně jejich přehledů.',
'Vytvoření návrhů míst pro setkávání s občany a cestu k jejich úspěšné realizaci.',
'Chceme identifikovat a postupně řešit specifické potřeby jednotlivých místních částí.',
'Podpoříme budování nových sítí veřejného osvětlení a datových sítí s postupným ukládáním do země.',
'Budeme usilovat o vybudování splaškové kanalizace s jasně stanoveným harmonogramem realizace.']),
('Rozpočtová odpovědnost a plánování', [
'Prosazujeme odpovědné, transparentní hospodaření a dlouhodobé investiční plánování.',
'Aktivně budeme vyhledávat dotační příležitosti pro nové projekty.',
'Investiční priority chceme nastavovat podle skutečných potřeb obyvatel.']),
('Doprava a bezpečnost', [
'Budeme pečovat o místní komunikace, přechody a dopravní značení.',
'Zaměříme se na bezpečnost chodců, dětí a seniorů.',
'Podpoříme rozšiřování parkovacích míst tam, kde je to potřeba.',
'Chceme úzce spolupracovat se složkami IZS, BESIP a státní správou.']),
('Školství, rodiny a mládež', [
'Podpoříme rozvoj mateřské a základní školy.',
'Budeme usilovat o opravu a navýšení kapacit základní školy.',
'Zaměříme se na bezpečné trasy do škol.',
'Podpoříme volnočasové aktivity a zájmové kroužky.',
'Budeme rozvíjet dětská hřiště a prostory pro mladé lidi.']),
('Senioři a sociální oblast', [
'Chceme podporovat dostupné služby pro seniory a osoby se sníženou soběstačností.',
'Podpoříme mezigenerační spolupráci a společenské aktivity pro všechny generace.']),
('Životní prostředí a obecní zeleň', [
'Budeme pečovat o veřejnou zeleň, parky a lesy.',
'Zaměříme se na kvalitní a efektivní systém odpadového hospodářství.',
'Podpoříme údržbu krajiny, vodních toků a výsadbu nové zeleně tam, kde to bude vhodné a přínosné.']),
('Kultura, tradice a spolky', [
'Budeme podporovat kulturní, společenské a obecní akce.',
'Chceme aktivně spolupracovat s místními spolky.',
'Budeme chránit a rozvíjet místní tradice.']),
('Sport a volnočasové aktivity', [
'Zaměříme se na rozvoj a údržbu sportovních areálů.',
'Podpoříme amatérské sportovní skupiny a místní sportovní aktivity.',
'Budeme pečovat o síť stezek pro pěší a cyklisty.',
'Chceme vytvářet kvalitní veřejný prostor pro rodiny, děti i aktivní občany.']),
('Podpora podnikání a místních služeb', [
'Chceme výrazně zlepšit spolupráci podnikatelů s obcí.',
'Budeme vytvářet podmínky pro rozvoj služeb, řemesel, obchodů a gastronomie.'])]

header = '''<a class="skip" href="#obsah">Přeskočit na obsah</a>
<header class="top"><div class="wrap header-inner"><a class="brand" href="index.html" aria-label="Tršicko – úvodní stránka"><strong>TRŠICKO</strong><span>obce pro život</span></a><nav class="nav" aria-label="Hlavní navigace"><a href="index.html#o-nas">O nás</a><a href="index.html#program">Program</a><a href="index.html#kandidati">Kandidáti</a><a class="nav-event" href="index.html#setkani">Setkání 4. října ↗</a></nav></div></header>'''
footer = '''<footer><div class="wrap footer-inner"><a class="brand" href="index.html"><strong>TRŠICKO</strong><span>obce pro život</span></a><p>Tršicko – obce pro život · Komunální volby 2026</p><a href="index.html#dokumenty">Dokumenty ke stažení ↑</a></div></footer>'''

def page(title, description, body):
    return f'''<!doctype html>
<html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(title)}</title><meta name="description" content="{escape(description)}"><meta name="theme-color" content="#09264b"><link rel="icon" type="image/webp" href="assets/logo.webp"><link rel="stylesheet" href="styles.css"></head><body>{header}{body}{footer}</body></html>'''

cards = []
names = []
for source in sorted((SOURCE / 'Portréty').iterdir(), key=lambda p: int(p.name.split('.')[0]) if not p.name.startswith('.') else 999):
    if source.name.startswith('.'):
        continue
    number = int(source.name.split('.')[0])
    name = source.stem.split('.', 1)[1].strip()
    names.append(name)
    asset = optimize(source, f'kandidat-{number:02d}.webp', 1100)
    cards.append(f'''<a class="candidate" href="kandidat-{number:02d}.html"><div class="portrait"><img src="assets/{asset}" alt="{escape(name)}" width="1100" height="1650" loading="lazy"><span class="candidate-number">{number:02d}</span></div><h3>{escape(name)}</h3><p>Zobrazit profil <span aria-hidden="true">↗</span></p></a>''')
    candidate_page = f'''<main id="obsah" class="article"><a class="back" href="index.html#kandidati">← Zpět na kandidátku</a><p class="eyebrow">Volební číslo sdružení 2 · Pořadí na kandidátce {number}</p><h1>{escape(name)}</h1><p class="source-note">Kandidátský profil sdružení Tršicko – obce pro život.</p><img src="assets/{asset}" alt="Kandidátský profil: {escape(name)} – zkušenosti a představení" width="1100" height="1650"><p><a href="assets/{asset}">Otevřít profil v plné velikosti ↗</a></p></main>'''
    (PUBLIC / f'kandidat-{number:02d}.html').write_text(page(f'{name} | Tršicko', f'Kandidátský profil – {name}. Tršicko – obce pro život, komunální volby 2026.', candidate_page), encoding='utf-8')

program_html = ''.join(f'''<details class="program-item"><summary><span class="number">{i:02d}</span>{escape(title)}</summary><ul>{''.join(f'<li>{escape(item)}</li>' for item in items)}</ul></details>''' for i, (title, items) in enumerate(program, 1))
body = '''<main id="obsah">
<section class="hero"><div class="wrap hero-grid"><div><p class="eyebrow">Komunální volby 2026</p><p class="ballot-number"><span>Volební číslo</span><strong>2</strong></p><h1>TRŠICKO<span>obce pro život.</span></h1><p class="lead">Program pro obec Tršice a její místní části.<br>Období 2026–2030.</p><div class="actions"><a class="button" href="#program">Volební program <span aria-hidden="true">↗</span></a><a class="button secondary" href="#kandidati">Kandidátka <span aria-hidden="true">↓</span></a></div></div><div class="hero-mark"><img src="assets/logo.webp" alt="Tršicko – obce pro život. Společně tvoříme naše obce lepší." width="700" height="700" fetchpriority="high"><div class="hero-caption"><strong>Tršicko – obce pro život</strong><span>2026–2030</span></div></div></div></section>
<div class="villages"><div class="wrap"><span>Tršice</span><span>Lipňany</span><span>Zákřov</span><span>Vacanovice</span><span>Přestavlky</span><span>Hostkovice</span></div></div>
<section class="section" id="o-nas"><div class="wrap intro-grid"><div><p class="eyebrow">O sdružení</p><h2>Úvodní slovo</h2></div><div class="intro-copy"><p><strong>Milí sousedé,</strong></p><p>rádi bychom vám představili nové sdružení Tršicko – obce pro život a našich jedenáct kandidátů pro nadcházející volby do zastupitelstva obce.</p><details><summary>Přečíst celé úvodní slovo</summary><p>Spojuje nás jednoduchá myšlenka: chceme obce, ve kterých se dá dobře, bezpečně a aktivně žít. Obce, kde se lidé znají, vzájemně si pomáhají a kde má každý prostor podílet se na jejich budoucnosti.</p><p>Nechceme dělat politiku. Chceme poctivě pracovat pro blaho našich obcí, naslouchat vašim podnětům a hledat řešení, která budou dávat smysl dnes i v dalších letech.</p><p>Jsme připraveni spolupracovat s dalšími kandidáty z ostatních sdružení i s vámi, našimi sousedy. Věříme, že dobré věci vznikají tehdy, když se dokážeme domluvit, respektovat se a spojit síly pro společný cíl.</p><p>Každý z našich kandidátů přináší zkušenosti ze svého zaměstnání, spolků i každodenního života v našich obcích. Aktivně se podílíme na jejich činnosti a chceme své schopnosti a energii využít také ve prospěch celé obce.</p><p>Společně se chceme podílet na dalším zlepšování kvality života ve všech našich obcích – v Tršicích, Lipňanech, Zákřově, Vacanovicích, Přestavlkách i Hostkovicích. Záleží nám na bezpečném prostředí, péči o veřejný prostor, rozumném rozvoji i zachování místních tradic.</p><p>Budeme rádi za vaši důvěru a váš hlas v nadcházejících komunálních volbách.</p><p><strong>Jsme tu pro vás.<br>TRŠICKO-obce pro život<br>Společně tvoříme naše obce lepší.</strong></p><a class="text-link" href="assets/uvodni-slovo.webp">Původní úvodní slovo ↗</a></details></div></div></section>
<section class="section pale" id="program"><div class="wrap"><div class="section-head"><div><p class="eyebrow">Program 2026–2030</p><h2>Volební program</h2></div><p>Program pro obec Tršice a její místní části.</p></div><div class="program-grid">''' + program_html + '''</div><div class="program-bottom"><a class="button" href="program.html">Podrobný program <span aria-hidden="true">↗</span></a><a class="text-link" href="assets/program-2026-2030.pdf">Program ke stažení v PDF ↓</a></div></div></section>
<section class="section" id="kandidati"><div class="wrap"><div class="section-head"><div><p class="eyebrow">Kandidátka 2026</p><h2>Kandidáti sdružení</h2></div><p>Volební číslo sdružení: <strong>2</strong>.<br>Jedenáct kandidátů do zastupitelstva obce.</p></div><div class="candidates">''' + ''.join(cards) + '''</div></div></section>
<section class="section event-section" id="setkani"><div class="wrap"><div class="event"><div><p class="eyebrow">Setkání s občany</p><h2>Pozvánka na<br>přátelské setkání</h2><p>Setkání sdružení Tršicko – obce pro život se všemi kandidáty, představením programu a vizualizací podoby některých částí obcí.</p><p>Host setkání: <strong>Ing. Jan Koudelka</strong>, projektový ředitel společnosti Reticulum.</p><div class="actions"><a class="button" href="assets/pozvanka.webp">Zobrazit pozvánku <span aria-hidden="true">↗</span></a></div></div><div class="event-info"><time class="event-date" datetime="2026-10-04T15:00:00+02:00">4. října 2026</time><dl><dt>Den</dt><dd>Neděle</dd><dt>Začátek</dt><dd>15:00</dd><dt>Místo</dt><dd>Společenský sál<br>v Tršicích</dd></dl></div></div></div></section>
<section class="section pale" id="dokumenty"><div class="wrap"><div class="section-head"><div><p class="eyebrow">Ke stažení</p><h2>Dokumenty</h2></div></div><div class="downloads"><a class="download" href="assets/program-2026-2030.pdf"><div><strong>Volební program</strong><small>PDF · 7,7 MB</small></div><span class="arrow" aria-hidden="true">↓</span></a><a class="download" href="assets/kandidatka.pdf"><div><strong>Kandidátka</strong><small>PDF · 5,4 MB</small></div><span class="arrow" aria-hidden="true">↓</span></a><a class="download" href="assets/pozvanka.webp"><div><strong>Pozvánka na setkání</strong><small>Obrázek · 4. října 2026</small></div><span class="arrow" aria-hidden="true">↗</span></a></div></div></section></main>'''
(PUBLIC / 'index.html').write_text(page('Tršicko – obce pro život | Volby 2026', 'Sdružení Tršicko – obce pro život. Kandidátka, program 2026–2030 a setkání s občany v Tršicích.', body), encoding='utf-8')

ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
docx = next(SOURCE.glob('*.docx'))
with ZipFile(docx) as archive:
    xml = ET.fromstring(archive.read('word/document.xml'))
paragraphs = [''.join(t.text or '' for t in p.findall('.//w:t', ns)).strip() for p in xml.findall('.//w:p', ns)]
headings = {'Plánování', 'Budovy a pozemky', 'Výsadba a údržba veřejného prostranství', 'Zdroje vody', 'Komunikace občan a úřad', 'Odpady a bioodpady', 'Spolky', 'JPO obce Tršice', 'Priority našeho sdružení pro období 2026–2030', 'Základní a mateřská škola Tršice a SVP Tršice', 'Rozvoj a podpora zaměstnanců naší obce', 'Finance', 'Sportoviště a dětská hřiště', 'Služby'}
content = []
for p in paragraphs:
    if not p or p in {'PROGRAM NAŠEHO SDRUŽENÍ', '2026–2030'}:
        continue
    tag = 'h2' if p in headings else 'p'
    content.append(f'<{tag} class="source-paragraph">{escape(p)}</{tag}>')
full_program = '''<main id="obsah" class="article"><a class="back" href="index.html#program">← Zpět na přehled programu</a><p class="eyebrow">Období 2026–2030</p><h1>Program našeho sdružení</h1><p class="source-note">Podrobný program sdružení Tršicko – obce pro život. <a href="assets/program-2026-2030.pdf">Stručný program v PDF ↓</a></p>''' + ''.join(content) + '</main>'
(PUBLIC / 'program.html').write_text(page('Podrobný program 2026–2030 | Tršicko', 'Podrobný program sdružení Tršicko – obce pro život pro období 2026–2030.', full_program), encoding='utf-8')
(PUBLIC / '404.html').write_text(page('Stránka nenalezena | Tršicko', 'Požadovanou stránku se nepodařilo najít.', '<main id="obsah" class="article"><p class="eyebrow">Chyba 404</p><h1>Stránka nenalezena</h1><p>Tato adresa na webu není dostupná.</p><a class="button" href="index.html">Přejít na úvodní stránku</a></main>'), encoding='utf-8')
print(f'Generated home, program and {len(names)} candidate pages. Source paragraphs: {len(content)}.')
