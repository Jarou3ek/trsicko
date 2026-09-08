# Tršicko – obce pro život

Web sdružení pro komunální volby 2026. Statický web bez externích závislostí, JavaScriptu v prohlížeči, cookies a měření návštěvnosti.

## Obsah

- Úvod, představení sdružení a deset oblastí programu.
- Samostatná stránka s úplným textem dodaného podrobného programu.
- Jedenáct kandidátů a samostatné stránky s dodanými kandidátskými profily.
- Pozvánka na setkání 4. října 2026 v 15:00 ve Společenském sále v Tršicích.
- Program a kandidátka v PDF.

Texty jsou převzaty z podkladů, nikoliv nezávisle ověřené. Obrázky jsou optimalizovány pro web. Původní soubory ve složce `podklady` se nemění.

## Cloudflare Pages – propojení s GitHubem

V Cloudflare otevřete **Workers & Pages → Create application → Pages → Import an existing Git repository** a vyberte `Jarou3ek/trsicko`.

| Nastavení | Hodnota |
| --- | --- |
| Production branch | `main` |
| Framework preset | `None` |
| Root directory | ponechat prázdné |
| Build command | `node scripts/build.mjs` |
| Build output directory | `dist` |

Poté **Save and Deploy**. Po úspěšném nasazení Cloudflare přidělí adresu `*.pages.dev`. Vlastní doménu přidejte v nastavení projektu v **Custom domains**. Další změny v `main` se automaticky nasadí.

[Oficiální návod](https://developers.cloudflare.com/pages/get-started/git-integration/)

Projekt je určen pro **Pages**, nikoliv pro průvodce nasazením Workeru s příkazem `wrangler deploy`. Soubor `wrangler.jsonc` popisuje výstup Pages.

## Úpravy

- `public/styles.css` – vzhled a responzivní rozvržení.
- `public/*.html` – hotové stránky připravené k publikaci.
- `public/assets` – optimalizované obrázky a dokumenty.
- `scripts/prepare_content.py` – opakovatelné sestavení obsahu z podkladů (Python + Pillow). Obsahuje přepis úvodního slova a stručného programu. Při přímých úpravách HTML upravte také generátor, jinak by je jeho další spuštění přepsalo.
- `scripts/build.mjs` – ověření lokálních odkazů a vytvoření `dist`. Vyžaduje Node.js 22 nebo novější, nemá závislosti.

Lokální sestavení: `node scripts/build.mjs`.
Lokální náhled s Pythonem: `python -m http.server 4173 --directory public`.

## K doplnění

- Veřejný kontaktní e-mail, případně potvrzený odkaz na Facebook a doména.
- Ověřit příjmení kandidáta č. 9: osobní profil a název souboru uvádějí **Lukáš Veiser**, společný plakát **Lukáš Weiser**. Web prozatím používá zápis z osobního profilu.
- Podrobné kandidátské medailonky jsou dodané jako obrázky. Pro plnou čitelnost asistivními technologiemi je vhodné doplnit schválené textové přepisy.

Nasazení do Cloudflare a připojení domény vyžadují přístup do příslušného Cloudflare účtu; samotné uložení na GitHub web nespouští.
