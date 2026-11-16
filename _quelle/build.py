# Baut arm.swiss als statische Seite in EN (Hauptsprache) und DE.
# Grundlage: Skill arm-brand, Design-System «ARM»; Texte aus Website-Konzept v1.3, Gestaltung neu (15.11.2026).
# Aufruf: python3 _quelle/build.py <zielordner>
import os, sys, html, json, shutil, urllib.parse

OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/arm/site"
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://www.arm.swiss"
CSS_V = "4"
E = html.escape

ADDR = "Arm AG · Unterer Mattenweg 11 · 3920 Zermatt"
MAIL = "rh@arm.swiss"
TEL = "+41 79 221 11 93"
TEL_HREF = "+41792211193"
LINKEDIN = "https://www.linkedin.com/company/armswiss/"

FIELDS = {
"en": [
  ("Origination", "For investors, family offices and operators.",
   "Assets and projects found against a written search profile, often before they reach the market. With a market map, a monthly report and a review after six months."),
  ("Investor &amp; Operator Readiness", "For owners, developers and project sponsors.",
   "An asset or project prepared so that investors and operators can decide: market, property, options, operating model, a ten-year business plan and a clear recommendation."),
  ("Capital Introduction", "For developers, owners and project sponsors.",
   "Personal introductions to investors, lenders and operators who fit the project, on the basis of sound documents, up to a letter of intent."),
  ("Market Entry &amp; Expansion", "For operators, brands and service partners.",
   "Positioning, a target list and personal introductions to owners and decision-makers. In Switzerland, or from Switzerland abroad."),
  ("Strategic Counsel", "For owners, boards and investors.",
   "A confidential second opinion and support in negotiations. Month by month, or for a defined project."),
  ("Destinations &amp; Public Sector", "For municipalities and tourism organisations.",
   "Which properties in a place are secure, which are at risk, and what to do about it. With a roadmap for the next five years."),
],
"de": [
  ("Origination", "Für Investoren, Family Offices und Betreiber.",
   "Objekte und Projekte nach einem schriftlichen Suchprofil, oft bevor sie auf dem Markt sind. Mit Marktkarte, einem Bericht jeden Monat und einer Standortbestimmung nach sechs Monaten."),
  ("Investor &amp; Operator Readiness", "Für Eigentümer, Entwickler und Projektträger.",
   "Ein Objekt oder Projekt so aufbereitet, dass Investoren und Betreiber entscheiden können: Markt, Liegenschaft, Optionen, Betriebsmodell, Businessplan über zehn Jahre und eine klare Empfehlung."),
  ("Capital Introduction", "Für Entwickler, Eigentümer und Projektträger.",
   "Persönliche Einführung bei Investoren, Kreditgebern und Betreibern, die zum Projekt passen. Auf der Grundlage sauberer Unterlagen, bis zur Absichtserklärung."),
  ("Market Entry &amp; Expansion", "Für Betreiber, Marken und Dienstleister.",
   "Positionierung, Zielliste und persönliche Einführung bei Eigentümern und Entscheidern. In der Schweiz oder von der Schweiz aus."),
  ("Strategic Counsel", "Für Eigentümer, Verwaltungsräte und Investoren.",
   "Eine vertrauliche Zweitmeinung und Begleitung in Verhandlungen. Monatlich oder für ein bestimmtes Vorhaben."),
  ("Destinationen und öffentliche Hand", "Für Gemeinden und Tourismusorganisationen.",
   "Welche Betriebe im Ort gesichert sind, welche gefährdet und was zu tun ist. Mit einem Fahrplan für die nächsten fünf Jahre."),
],
}

T = {
"en": {
  "lang": "en", "path": "/", "other": "/de/", "other_label": "DE", "other_name": "Deutsch",
  "title": "ARM | Private Office",
  "desc": "ARM – Private Office in Zermatt connects investors, developers, operators and public institutions, in Switzerland and internationally. Hotels and resorts, serviced and branded residences, workation and mixed-use sites.",
  "nav": [("#work", "Work"), ("#approach", "Approach"), ("#origins", "Origins"), ("#contact", "Contact")],
  "ids": ["work", "approach", "origins", "contact"],
  "home": "ARM – Private Office, home",
  "h1": "Private Office",
  "sub": "Connecting investors, developers, operators and public institutions. In Switzerland and internationally.",
  "lead": "ARM finds assets and projects, makes them ready for investors and operators, brings capital and partners to the table and stands beside owners when decisions are due.",
  "lead2": "Hotels and resorts, serviced and branded residences, workation and mixed-use sites, and the places they belong to.",
  "h_work": "What ARM does",
  "lex": "Swiss hotels are generally exempt from the Lex Koller; residential parts are not. Each case is checked with a lawyer.",
  "h_way": "How ARM works",
  "way": [
    ("Discreet.", "Names, figures and intentions stay with the people concerned. ARM does not publish mandates."),
    ("From Switzerland.", "Based in Zermatt, connected to investors and operators across Europe, the Gulf and beyond."),
    ("Clear.", "A written mandate, a fixed fee or retainer, regular reporting. No remuneration from third parties without the client’s knowledge."),
    ("By referral.", "Most mandates begin with an introduction from someone who knows the work."),
  ],
  "h_origin": "Since 1861",
  "origin": "In 1861 Friedrich Arm founded a reed-making workshop in Biglen, near Bern. Five generations built hand looms there. Today Arm AG is the private office of Roman Haller in Zermatt. The name has stayed.",
  "h_contact": "Contact",
  "contact_lead": "Every conversation is confidential.",
  "mail_subject": "Enquiry via arm.swiss",
  "country": "Switzerland",
  "imprint": ("Imprint", "/legal-notice/"), "privacy": ("Privacy", "/privacy-policy/"),
  "back": "Back to the home page",
  "notfound_t": "Page not found",
  "notfound": "This page does not exist, or no longer exists.",
},
"de": {
  "lang": "de-CH", "path": "/de/", "other": "/", "other_label": "EN", "other_name": "English",
  "title": "ARM | Private Office",
  "desc": "ARM – Private Office in Zermatt verbindet Investoren, Entwickler, Betreiber und öffentliche Institutionen, in der Schweiz und international. Hotels und Resorts, bewirtschaftete Wohnungen und Branded Residences, Workation und gemischt genutzte Areale.",
  "nav": [("#arbeit", "Arbeit"), ("#haltung", "Haltung"), ("#herkunft", "Herkunft"), ("#kontakt", "Kontakt")],
  "ids": ["arbeit", "haltung", "herkunft", "kontakt"],
  "home": "ARM – Private Office, Startseite",
  "h1": "Private Office",
  "sub": "Verbindet Investoren, Entwickler, Betreiber und öffentliche Hand. In der Schweiz und international.",
  "lead": "ARM findet Objekte und Projekte, macht sie bereit für Investoren und Betreiber, bringt Kapital und Partner an den Tisch und steht Eigentümern zur Seite, wenn es zu entscheiden gilt.",
  "lead2": "Hotels und Resorts, bewirtschaftete Wohnungen und Branded Residences, Workation und gemischt genutzte Areale, und die Orte, zu denen sie gehören.",
  "h_work": "Was ARM macht",
  "lex": "Hotels in der Schweiz sind von der Lex Koller grundsätzlich ausgenommen, Wohnanteile nicht. Jeder Fall wird mit einem Anwalt geprüft.",
  "h_way": "Wie ARM arbeitet",
  "way": [
    ("Diskret.", "Namen, Zahlen und Absichten bleiben bei den Beteiligten. ARM veröffentlicht keine Mandate."),
    ("Von der Schweiz aus.", "Sitz in Zermatt, vernetzt mit Investoren und Betreibern in Europa, am Golf und darüber hinaus."),
    ("Klar.", "Ein schriftliches Mandat, ein fester Preis oder Retainer, regelmässige Berichte. Keine Entschädigung von Dritten ohne Wissen des Auftraggebers."),
    ("Auf Empfehlung.", "Die meisten Mandate beginnen mit einer Empfehlung von jemandem, der die Arbeit kennt."),
  ],
  "h_origin": "Seit 1861",
  "origin": "1861 gründete Friedrich Arm in Biglen bei Bern eine Blattmacherei. Fünf Generationen bauten dort Webstühle. Heute ist die Arm AG das Private Office von Roman Haller in Zermatt. Der Name ist geblieben.",
  "h_contact": "Kontakt",
  "contact_lead": "Ein Gespräch ist vertraulich.",
  "mail_subject": "Anfrage über arm.swiss",
  "country": "Schweiz",
  "imprint": ("Impressum", "/de/impressum/"), "privacy": ("Datenschutz", "/de/datenschutz/"),
  "back": "Zur Startseite",
  "notfound_t": "Seite nicht gefunden",
  "notfound": "Diese Seite gibt es nicht oder nicht mehr.",
},
}

LEGAL = {
"en": {
  "imprint": ("Imprint", [
    ("Arm AG", f"Unterer Mattenweg 11<br>3920 Zermatt<br>Switzerland<br>Phone <a href=\"tel:{TEL_HREF}\">{TEL}</a><br>E-mail <a href=\"mailto:{MAIL}\">{MAIL}</a>"),
    ("Register", "Commercial register of the Canton of Valais<br>UID CHE-101.346.536<br>Responsible for content: Roman Haller"),
    ("No offer", "The content of this website is for information only. It is not an offer, not investment advice and not legal or tax advice."),
    ("Liability", "The content of this website has been prepared with care. No guarantee is given as to its accuracy, completeness or currency. Arm AG is not responsible for the content of external websites linked from this site."),
    ("Copyright", "Texts and the ARM monogram are protected. Any use beyond the limits of copyright law requires the prior written consent of Arm AG."),
  ]),
  "privacy": ("Privacy", [
    ("Controller", f"Arm AG, Unterer Mattenweg 11, 3920 Zermatt, Switzerland, <a href=\"mailto:{MAIL}\">{MAIL}</a>"),
    ("This website", "This website sets no cookies, uses no analytics or tracking tools and loads no fonts or content from third parties."),
    ("Hosting", "The website is hosted on GitHub Pages (GitHub Inc., USA). When a page is requested, GitHub processes technically necessary data such as the IP address, time and requested page in order to deliver and protect the site. This data may be processed in the United States."),
    ("E-mail and phone", "If you write or call, Arm AG uses your details only to handle your enquiry. E-mail is provided by Microsoft 365. Data is not passed on to third parties without your consent unless the law requires it."),
    ("Your rights", f"Under the Swiss Federal Act on Data Protection (FADP) you may request information about your data, its correction or its deletion. Please write to <a href=\"mailto:{MAIL}\">{MAIL}</a>."),
    ("Version", "November 2026"),
  ]),
},
"de": {
  "imprint": ("Impressum", [
    ("Arm AG", f"Unterer Mattenweg 11<br>3920 Zermatt<br>Schweiz<br>Telefon <a href=\"tel:{TEL_HREF}\">{TEL}</a><br>E-Mail <a href=\"mailto:{MAIL}\">{MAIL}</a>"),
    ("Handelsregister", "Handelsregister des Kantons Wallis<br>UID CHE-101.346.536<br>Verantwortlich für den Inhalt: Roman Haller"),
    ("Kein Angebot", "Die Inhalte dieser Website dienen der Information. Sie sind kein Angebot, keine Anlageempfehlung und keine Rechts- oder Steuerauskunft."),
    ("Haftung", "Die Inhalte dieser Website sind mit Sorgfalt erstellt. Für Richtigkeit, Vollständigkeit und Aktualität besteht keine Gewähr. Für die Inhalte verlinkter Websites ist die Arm AG nicht verantwortlich."),
    ("Urheberrecht", "Texte und das ARM-Monogramm sind geschützt. Jede Verwendung über das Urheberrecht hinaus braucht die vorgängige schriftliche Zustimmung der Arm AG."),
  ]),
  "privacy": ("Datenschutz", [
    ("Verantwortlich", f"Arm AG, Unterer Mattenweg 11, 3920 Zermatt, Schweiz, <a href=\"mailto:{MAIL}\">{MAIL}</a>"),
    ("Diese Website", "Diese Website setzt keine Cookies, verwendet keine Analyse- oder Trackingwerkzeuge und lädt keine Schriften oder Inhalte von Dritten."),
    ("Hosting", "Die Website liegt bei GitHub Pages (GitHub Inc., USA). Beim Aufruf verarbeitet GitHub technisch notwendige Daten wie IP-Adresse, Zeitpunkt und aufgerufene Seite, um die Seite auszuliefern und zu schützen. Diese Daten können in den USA bearbeitet werden."),
    ("E-Mail und Telefon", "Wer schreibt oder anruft, dessen Angaben verwendet die Arm AG nur, um die Anfrage zu bearbeiten. Die E-Mails laufen über Microsoft 365. Ohne Einwilligung gehen keine Daten an Dritte, ausser das Gesetz verlangt es."),
    ("Ihre Rechte", f"Nach dem Datenschutzgesetz (DSG) können Sie Auskunft über Ihre Daten, deren Berichtigung oder Löschung verlangen. Schreiben Sie an <a href=\"mailto:{MAIL}\">{MAIL}</a>."),
    ("Stand", "November 2026"),
  ]),
},
}
LEGAL_PATH = {"en": {"imprint": "/legal-notice/", "privacy": "/privacy-policy/"},
              "de": {"imprint": "/de/impressum/", "privacy": "/de/datenschutz/"}}

def svg(name):
    return open(os.path.join(HERE, "assets", name)).read().strip()

def head(t, title, desc, path, alt_paths):
    alts = "".join(f'<link rel="alternate" hreflang="{h}" href="{BASE}{p}">' for h, p in alt_paths)
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{BASE}{path}">
{alts}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#FFFFFF">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ARM – Private Office">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{BASE}{path}">
<meta property="og:image" content="{BASE}/img/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ARM monogram">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/style.css?v={CSS_V}">
</head>
<body>
<a class="skip" href="#main">{'Skip to content' if t['lang']=='en' else 'Zum Inhalt'}</a>
"""

def header(t, nav=True, other=None, dark=False):
    links = "".join(f'<a href="{t["path"]}{h}">{E(l)}</a>' for h, l in t["nav"]) if nav else ""
    other = other or t["other"]
    mark = svg('monogramm-weiss.svg') if dark else svg('monogramm.svg')
    cls = "top top-dark" if dark else "top"
    return f"""<header class="{cls}"><div class="wrap top-in">
<a class="mark" href="{t['path']}" aria-label="{E(t['home'])}">{mark}</a>
<nav class="nav" aria-label="{'Main' if t['lang']=='en' else 'Hauptnavigation'}">{links}<a class="lang" href="{other}" hreflang="{'de' if t['lang']=='en' else 'en'}" lang="{'de' if t['lang']=='en' else 'en'}" title="{t['other_name']}">{t['other_label']}</a></nav>
</div></header>
"""

def footer(t, lang):
    im, pr = t["imprint"], t["privacy"]
    return f"""<footer class="foot"><div class="wrap foot-in">
<p>{ADDR} · {t['country']}</p>
<p class="foot-links"><a href="{im[1]}">{im[0]}</a><a href="{pr[1]}">{pr[0]}</a><a href="{LINKEDIN}" rel="noopener">LinkedIn</a></p>
</div></footer>
</body>
</html>
"""

def jsonld():
    d = {"@context": "https://schema.org", "@type": "Organization", "name": "ARM – Private Office",
         "legalName": "Arm AG", "url": BASE + "/", "logo": BASE + "/img/arm-monogramm-512.png",
         "foundingDate": "1861", "email": MAIL, "telephone": TEL,
         "address": {"@type": "PostalAddress", "streetAddress": "Unterer Mattenweg 11", "postalCode": "3920",
                     "addressLocality": "Zermatt", "addressRegion": "VS", "addressCountry": "CH"},
         "sameAs": [LINKEDIN]}
    return f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>\n'

def home(lang):
    t = T[lang]; f = FIELDS[lang]; ids = t["ids"]
    cards = "".join(
        f'<li class="field"><h3>{n}</h3><p class="who">{E(w)}</p><p>{E(x)}</p></li>'
        for n, w, x in f)
    way = "".join(f'<li><h3>{E(k)}</h3><p>{E(v)}</p></li>' for k, v in t["way"])
    mailto = f"mailto:{MAIL}?subject={urllib.parse.quote(t['mail_subject'])}"
    alts = [("en", "/"), ("de", "/de/"), ("x-default", "/")]
    return (head(t, t["title"], t["desc"], t["path"], alts) + f"""<div class="hero">
""" + header(t, dark=True) + f"""<div class="wrap hero-in">
<h1>{t['h1']}</h1>
<p class="sub">{E(t['sub'])}</p>
</div>
</div>
<main id="main">
<section class="intro"><div class="wrap grid">
<p class="statement">{E(t['lead'])}</p>
<p class="statement-2">{E(t['lead2'])}</p>
</div></section>

<section class="sec" id="{ids[0]}"><div class="wrap">
<h2 class="h2">{E(t['h_work'])}</h2>
<ul class="fields">{cards}</ul>
<p class="note">{E(t['lex'])}</p>
</div></section>

<section class="sec sec-grey" id="{ids[1]}"><div class="wrap grid">
<h2 class="h2 col-a">{E(t['h_way'])}</h2>
<ul class="way col-b">{way}</ul>
</div></section>

<section class="origin" id="{ids[2]}"><div class="wrap grid">
<h2 class="origin-h col-a">{E(t['h_origin'])}</h2>
<p class="origin-t col-b">{E(t['origin'])}</p>
</div></section>

<section class="sec contact" id="{ids[3]}"><div class="wrap grid">
<h2 class="h2 col-a">{E(t['h_contact'])}</h2>
<div class="col-b">
<p class="contact-lead">{E(t['contact_lead'])}</p>
<p class="mail"><a href="{mailto}">{MAIL}</a></p>
<p class="phone"><a href="tel:{TEL_HREF}">{TEL}</a></p>
<p class="who-c">Roman Haller</p>
</div>
</div></section>
</main>
""" + jsonld() + footer(t, lang))

def legal(lang, kind):
    t = T[lang]; title, blocks = LEGAL[lang][kind]
    path = LEGAL_PATH[lang][kind]
    other_lang = "de" if lang == "en" else "en"
    other = LEGAL_PATH[other_lang][kind]
    alts = [("en", LEGAL_PATH["en"][kind]), ("de", LEGAL_PATH["de"][kind])]
    body = "".join(f'<div class="grid row"><h2 class="row-h col-a">{E(h)}</h2><p class="col-b">{b}</p></div>' for h, b in blocks)
    return (head(t, f"{title} | ARM", f"{title}, Arm AG, Zermatt", path, alts).replace(
        '<meta property="og:type"', '<meta name="robots" content="noindex,follow">\n<meta property="og:type"', 1)
        + header(t, nav=False, other=other) + f"""<main id="main">
<section class="page-head"><div class="wrap"><h1>{E(title)}</h1></div></section>
<section class="legal"><div class="wrap">{body}
<div class="grid row"><p class="col-b"><a href="{t['path']}">{E(t['back'])}</a></p></div>
</div></section>
</main>
""" + footer(t, lang))

def notfound():
    t = T["en"]; d = T["de"]
    return (head(t, "Page not found | ARM", t["notfound"], "/404.html", []).replace(
        '<meta property="og:type"', '<meta name="robots" content="noindex">\n<meta property="og:type"', 1)
        + header(t, nav=False) + f"""<main id="main">
<section class="page-head"><div class="wrap">
<h1>{t['notfound_t']}</h1>
<p class="sub-l">{t['notfound']}</p>
<p class="sub-l" lang="de">{d['notfound']}</p>
<p class="back"><a href="/">{t['back']}</a></p>
</div></section>
</main>
""" + footer(t, "en"))

def write(rel, s, relative=True):
    # Root-relative Pfade in relative umschreiben, damit die Seite auch unter
    # roman-73-hub.github.io/arm.swiss/ (Vorschau) und unter www.arm.swiss läuft.
    if relative:
        depth = rel.strip("/").count("/") + (1 if rel.strip("/") and rel.endswith("/") else 0)
        pre = "../" * depth or "./"
        s = s.replace(' href="/', ' href="' + pre).replace(' src="/', ' src="' + pre)
    p = os.path.join(OUT, rel.lstrip("/"))
    if p.endswith("/"): p += "index.html"
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(s)

def main():
    os.makedirs(OUT, exist_ok=True)
    write("/", home("en")); write("/de/", home("de"))
    for lang in ("en", "de"):
        for kind in ("imprint", "privacy"):
            write(LEGAL_PATH[lang][kind], legal(lang, kind))
    write("/404.html", notfound(), relative=False)
    shutil.copy(os.path.join(HERE, "style.css"), os.path.join(OUT, "style.css"))
    shutil.copy(os.path.join(HERE, "assets", "favicon.svg"), os.path.join(OUT, "favicon.svg"))
    img = os.path.join(OUT, "img"); os.makedirs(img, exist_ok=True)
    for f in os.listdir(os.path.join(HERE, "assets")):
        if f.endswith(".png"):
            dst = img if f.startswith(("og", "arm-")) else OUT
            shutil.copy(os.path.join(HERE, "assets", f), os.path.join(dst, f))
    if os.environ.get("ARM_DOMAIN", "1") == "1":
        open(os.path.join(OUT, "CNAME"), "w").write("www.arm.swiss\n")
    elif os.path.exists(os.path.join(OUT, "CNAME")):
        os.remove(os.path.join(OUT, "CNAME"))
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    urls = ["/", "/de/"]
    sm = "".join(f"<url><loc>{BASE}{u}</loc></url>" for u in urls)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    print("ok", OUT)

if __name__ == "__main__":
    main()
