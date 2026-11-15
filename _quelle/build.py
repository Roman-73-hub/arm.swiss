# Baut arm.swiss als statische Seite in EN (Hauptsprache) und DE.
# Grundlage: ARM_20261114_Webseite-arm-swiss_Konzept_v1.3_DE-EN und Skill arm-brand.
# Aufruf: python3 _quelle/build.py <zielordner>
import os, sys, html, json, shutil, urllib.parse

OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/arm/site"
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://www.arm.swiss"
CSS_V = "1"
E = html.escape

ADDR = "Arm AG · Unterer Mattenweg 11 · 3920 Zermatt"
MAIL = "rh@arm.swiss"
TEL = "+41 79 221 11 93"
TEL_HREF = "+41792211193"
LINKEDIN = "https://www.linkedin.com/company/armswiss/"

FIELDS = {
"en": [
  ("Origination", "For investors, family offices and operators.",
   "Assets and projects found against a written search profile, often before they are offered. With a market map, monthly reporting and a review after six months."),
  ("Investor &amp; Operator Readiness", "For owners, developers and project sponsors.",
   "An asset or project made ready for investors and operators to decide: market, property, options, operating model, a ten-year business plan and a clear recommendation, in one report."),
  ("Capital Introduction", "For developers, owners and project sponsors.",
   "Introductions to investors, lenders and operators that fit the project, on the basis of investor-ready documents, up to a letter of intent."),
  ("Market Entry &amp; Expansion", "For operators, brands and service partners.",
   "Positioning, a target list and personal introductions to owners and decision-makers, in Switzerland or from Switzerland abroad."),
  ("Strategic Counsel", "For owners, boards and investors.",
   "A confidential second opinion and support in negotiations, as a monthly mandate or for a defined project."),
  ("Destinations &amp; Public Sector", "For municipalities and tourism organisations.",
   "Which properties in a destination are secure, which are at risk, and what to do about it. With a roadmap for the next five years."),
],
"de": [
  ("Origination", "Für Investoren, Family Offices und Betreiber.",
   "Objekte und Projekte nach schriftlichem Suchprofil, oft bevor sie angeboten werden. Mit Marktkarte, monatlichem Bericht und einer Standortbestimmung nach sechs Monaten."),
  ("Investor &amp; Operator Readiness", "Für Eigentümer, Entwickler und Projektträger.",
   "Ein Objekt oder Projekt, entscheidungsreif für Investoren und Betreiber: Markt, Liegenschaft, Optionen, Betriebsmodell, ein Businessplan über zehn Jahre und eine klare Empfehlung, in einem Bericht."),
  ("Capital Introduction", "Für Entwickler, Eigentümer und Projektträger.",
   "Einführung bei Investoren, Kreditgebern und Betreibern, die zum Projekt passen, auf der Grundlage investorentauglicher Unterlagen, bis zur Absichtserklärung."),
  ("Market Entry &amp; Expansion", "Für Betreiber, Marken und Dienstleister.",
   "Positionierung, Zielliste und persönliche Einführung bei Eigentümern und Entscheidern, in der Schweiz oder aus der Schweiz ins Ausland."),
  ("Strategic Counsel", "Für Eigentümer, Verwaltungsräte und Investoren.",
   "Eine vertrauliche Zweitmeinung und Begleitung in Verhandlungen, als Monatsmandat oder für ein bestimmtes Projekt."),
  ("Destinationen und öffentliche Hand", "Für Gemeinden und Tourismusorganisationen.",
   "Welche Betriebe in einer Destination gesichert sind, welche gefährdet und was zu tun ist. Mit einem Fahrplan für die nächsten fünf Jahre."),
],
}

T = {
"en": {
  "lang": "en", "path": "/", "other": "/de/", "other_label": "DE", "other_name": "Deutsch",
  "title": "ARM | Private Office",
  "desc": "ARM – Private Office in Zermatt connects investors, developers, operators and public institutions, in Switzerland and internationally. Hotels and resorts, serviced and branded residences, workation and mixed-use sites.",
  "nav": [("#fields", "Fields of work"), ("#way", "Way of working"), ("#contact", "Contact")],
  "home": "ARM – Private Office, home",
  "h1": "Private Office",
  "sub": "Connecting investors, developers, operators and public institutions. In Switzerland and internationally.",
  "lead": "ARM finds assets and projects, makes them ready for investors and operators, introduces capital and partners, and stands beside owners when decisions are due. Hotels and resorts, serviced and branded residences, workation and mixed-use sites, and the destinations around them.",
  "h_fields": "Fields of work",
  "lex": "Swiss hotels are generally exempt from the Lex Koller; residential parts are not. Each case is checked with a lawyer.",
  "h_way": "Way of working",
  "way": [
    ("Discreet.", "Names, figures and intentions stay with the people concerned. ARM does not publish mandates."),
    ("Switzerland at the core.", "Based in Zermatt, connected to investors and operators across Europe, the Gulf and beyond."),
    ("Defined.", "A written mandate, a fixed fee or retainer, regular reporting. No remuneration from third parties without the client’s knowledge."),
    ("By referral.", "Most mandates start with an introduction from someone who knows the work."),
  ],
  "h_contact": "Contact",
  "btn": "Get in touch",
  "mail_subject": "Enquiry via arm.swiss",
  "country": "Switzerland", "since": "Since 1861",
  "imprint": ("Imprint", "/legal-notice/"), "privacy": ("Privacy", "/privacy-policy/"),
  "back": "Back to the home page",
  "notfound_t": "Page not found",
  "notfound": "This page does not exist, or no longer exists.",
},
"de": {
  "lang": "de-CH", "path": "/de/", "other": "/", "other_label": "EN", "other_name": "English",
  "title": "ARM | Private Office",
  "desc": "ARM – Private Office in Zermatt verbindet Investoren, Entwickler, Betreiber und öffentliche Institutionen, in der Schweiz und international. Hotels und Resorts, bewirtschaftete Wohnungen und Branded Residences, Workation und gemischt genutzte Areale.",
  "nav": [("#geschaeftsfelder", "Geschäftsfelder"), ("#arbeitsweise", "Arbeitsweise"), ("#kontakt", "Kontakt")],
  "home": "ARM – Private Office, Startseite",
  "h1": "Private Office",
  "sub": "Verbindet Investoren, Entwickler, Betreiber und öffentliche Institutionen. In der Schweiz und international.",
  "lead": "ARM findet Objekte und Projekte, macht sie entscheidungsreif für Investoren und Betreiber, führt Kapital und Partner ein und steht Eigentümern zur Seite, wenn Entscheide anstehen. Hotels und Resorts, bewirtschaftete Wohnungen und Branded Residences, Workation und gemischt genutzte Areale sowie die Destinationen, in denen sie stehen.",
  "h_fields": "Geschäftsfelder",
  "lex": "Hotels in der Schweiz sind von der Lex Koller grundsätzlich ausgenommen, Wohnanteile nicht. Jeder Fall wird mit einem Anwalt geprüft.",
  "h_way": "Arbeitsweise",
  "way": [
    ("Diskret.", "Namen, Zahlen und Absichten bleiben bei den Beteiligten. ARM veröffentlicht keine Mandate."),
    ("Schweiz im Zentrum.", "Sitz in Zermatt, vernetzt mit Investoren und Betreibern in Europa, am Golf und darüber hinaus."),
    ("Klar geregelt.", "Ein schriftliches Mandat, ein Festpreis oder Retainer, regelmässiger Bericht. Keine Vergütung von Dritten ohne Wissen des Auftraggebers."),
    ("Auf Empfehlung.", "Die meisten Mandate beginnen mit einer Einführung durch jemanden, der die Arbeit kennt."),
  ],
  "h_contact": "Kontakt",
  "btn": "Kontakt aufnehmen",
  "mail_subject": "Anfrage über arm.swiss",
  "country": "Schweiz", "since": "Seit 1861",
  "imprint": ("Impressum", "/de/impressum/"), "privacy": ("Datenschutz", "/de/datenschutz/"),
  "back": "Zur Startseite",
  "notfound_t": "Seite nicht gefunden",
  "notfound": "Diese Seite gibt es nicht oder nicht mehr.",
},
}
T["en"]["ids"] = ["fields", "way", "contact"]
T["de"]["ids"] = ["geschaeftsfelder", "arbeitsweise", "kontakt"]

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

def header(t, nav=True, other=None):
    links = "".join(f'<a href="{t["path"]}{h}">{E(l)}</a>' for h, l in t["nav"]) if nav else ""
    other = other or t["other"]
    return f"""<header class="top"><div class="wrap top-in">
<a class="mark" href="{t['path']}" aria-label="{E(t['home'])}">{svg('monogramm.svg')}</a>
<nav class="nav" aria-label="{'Main' if t['lang']=='en' else 'Hauptnavigation'}">{links}<a class="lang" href="{other}" hreflang="{'de' if t['lang']=='en' else 'en'}" lang="{'de' if t['lang']=='en' else 'en'}" title="{t['other_name']}">{t['other_label']}</a></nav>
</div></header>
"""

def footer(t, lang):
    im, pr = t["imprint"], t["privacy"]
    return f"""<footer class="foot"><div class="wrap foot-in">
<p>{ADDR} · {t['country']} · {t['since']}</p>
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
    rows = "".join(
        f'<li class="field"><h3>{n}</h3><div><p class="who">{E(w)}</p><p>{E(x)}</p></div></li>'
        for n, w, x in f)
    way = "".join(f"<p><strong>{E(k)}</strong> {E(v)}</p>" for k, v in t["way"])
    mailto = f"mailto:{MAIL}?subject={urllib.parse.quote(t['mail_subject'])}"
    alts = [("en", "/"), ("de", "/de/"), ("x-default", "/")]
    return (head(t, t["title"], t["desc"], t["path"], alts) + header(t) + f"""<main id="main">
<section class="hero"><div class="wrap">
<h1>{t['h1']}</h1>
<p class="sub">{E(t['sub'])}</p>
<p class="lead">{E(t['lead'])}</p>
</div></section>

<section class="sec" id="{ids[0]}"><div class="wrap">
<div class="grid"><h2 class="col-h">{E(t['h_fields'])}</h2><div></div></div>
<ol class="fields">{rows}</ol>
<div class="grid"><div></div><p class="note">{E(t['lex'])}</p></div>
</div></section>

<section class="sec" id="{ids[1]}"><div class="wrap grid">
<h2 class="col-h">{E(t['h_way'])}</h2>
<div class="prose">{way}</div>
</div></section>

<section class="sec" id="{ids[2]}"><div class="wrap grid">
<h2 class="col-h">{E(t['h_contact'])}</h2>
<div class="prose contact">
<p><strong>Roman Haller</strong><br><a href="mailto:{MAIL}">{MAIL}</a> · <a href="tel:{TEL_HREF}">{TEL}</a></p>
<p><a class="btn" href="{mailto}">{E(t['btn'])}</a></p>
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
    body = "".join(f'<div class="grid row"><h2 class="col-h small">{E(h)}</h2><div class="prose"><p>{b}</p></div></div>' for h, b in blocks)
    return (head(t, f"{title} | ARM", f"{title}, Arm AG, Zermatt", path, alts).replace(
        '<meta property="og:type"', '<meta name="robots" content="noindex,follow">\n<meta property="og:type"', 1)
        + header(t, nav=False, other=other) + f"""<main id="main">
<section class="hero hero-s"><div class="wrap"><h1>{E(title)}</h1></div></section>
<section class="sec"><div class="wrap">{body}
<div class="grid row"><div></div><p><a href="{t['path']}">{E(t['back'])}</a></p></div>
</div></section>
</main>
""" + footer(t, lang))

def notfound():
    t = T["en"]; d = T["de"]
    return (head(t, "Page not found | ARM", t["notfound"], "/404.html", []).replace(
        '<meta property="og:type"', '<meta name="robots" content="noindex">\n<meta property="og:type"', 1)
        + header(t, nav=False) + f"""<main id="main">
<section class="hero"><div class="wrap">
<h1>{t['notfound_t']}</h1>
<p class="sub">{t['notfound']}</p>
<p class="lead" lang="de">{d['notfound']}</p>
<p><a class="btn" href="/">{t['back']}</a></p>
</div></section>
</main>
""" + footer(t, "en"))

def write(rel, s):
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
    write("/404.html", notfound())
    shutil.copy(os.path.join(HERE, "style.css"), os.path.join(OUT, "style.css"))
    shutil.copy(os.path.join(HERE, "assets", "favicon.svg"), os.path.join(OUT, "favicon.svg"))
    img = os.path.join(OUT, "img"); os.makedirs(img, exist_ok=True)
    for f in os.listdir(os.path.join(HERE, "assets")):
        if f.endswith(".png"):
            dst = img if f.startswith(("og", "arm-")) else OUT
            shutil.copy(os.path.join(HERE, "assets", f), os.path.join(dst, f))
    open(os.path.join(OUT, "CNAME"), "w").write("www.arm.swiss\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    urls = ["/", "/de/"]
    sm = "".join(f"<url><loc>{BASE}{u}</loc></url>" for u in urls)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    print("ok", OUT)

if __name__ == "__main__":
    main()
