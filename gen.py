"""Generates the inner pages of Inbal's portfolio from design coordinates."""
import os

OUT = "/home/claude/site/"
COL = 986  # content column width in the Figma frame (px)

BASE='https://inbalkeller.com/'
DESC={'index.html': 'Portfolio of Inbal Keller — musician (oboe) and Visual Communication Design student. UX/UI, illustration, motion and game design.', 'about.html': 'About Inbal Keller — 4th-year Visual Communication Design student, oboist, illustrator and ceramicist.', 'playground.html': 'Playground — illustrations, watercolor postcards, videos and experiments by Inbal Keller.', 'kabai.html': 'Kabai Hamangalim — a satirical Unity game designed and vibe-coded by Inbal Keller.', 'neighborhology.html': 'Neighborhology — an illustrated A2 data book on the neighborhoods of Tel Aviv, by Inbal Keller.', 'missp.html': "Miss Peregrine's Home for Peculiar Children — a title sequence by Inbal Keller.", 'dia.html': 'Dia — a UX/UI personal diabetes control dashboard, by Inbal Keller.'}
def META(page,title):
    d=DESC[page].replace('"','&quot;'); url=BASE+('' if page=='index.html' else page)
    return ('  <meta name="description" content="%s">\n  <link rel="canonical" href="%s">\n'
      '  <meta property="og:type" content="website">\n  <meta property="og:site_name" content="Inbal Keller">\n'
      '  <meta property="og:title" content="%s">\n  <meta property="og:description" content="%s">\n'
      '  <meta property="og:url" content="%s">\n  <meta property="og:image" content="%simages/share.jpg">\n'
      '  <meta property="og:image:width" content="1200">\n  <meta property="og:image:height" content="630">\n'
      '  <meta property="og:image:alt" content="Inbal Keller portfolio home page">\n'
      '  <meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:title" content="%s">\n'
      '  <meta name="twitter:description" content="%s">\n  <meta name="twitter:image" content="%simages/share.jpg">\n  <meta name="twitter:image:alt" content="Inbal Keller portfolio home page">\n'
      ) % (d,url,title,d,url,BASE,title,d,BASE)
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
{meta}  <link rel="preload" href="fonts/ibm-plex-mono-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="style.css?v=72">
  <script>
    /* a page that animated its own nav before leaving asks the next page to appear without a second transition */
    window.addEventListener('pagereveal', function (e) {{
      try {{ if (sessionStorage.getItem('vtSkip')) {{ sessionStorage.removeItem('vtSkip'); if (e.viewTransition) e.viewTransition.skipTransition(); }} }} catch (x) {{}}
    }});
  </script>
</head>
<body class="{theme}">
{mobile}
"""
FOOT = """
<script src="script.js?v=28"></script>
</body>
</html>
"""


MOBILE_ITEMS = [("about.html","About","box"),("playground.html","Playground","box"),(None,"Projects","group"),
    ("kabai.html","Kabai Hamangalim – Unity Gameplay","item"),("neighborhology.html","Neighborhology – Illustrated Infographics","item"),
    ("dia.html","Dia – UX|UI Diabetes Control Dashboard","item"),("missp.html","Miss P. Home for Peculiar – Title Sequence","item")]

def mobile(current):
    out=['  <!-- Mobile: bar + hamburger (replaces the side nav under 900px) -->',
         '  <header class="mobile-bar">',
         '    <a class="mobile-bar__name" href="index.html">Inbal Keller</a>',
         '    <button class="menu-toggle" id="menuToggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu">',
         '      <span class="menu-toggle__line"></span><span class="menu-toggle__line"></span><span class="menu-toggle__line"></span>',
         '    </button>','  </header>',
         '  <nav class="mobile-menu" id="mobileMenu" aria-label="Main menu">']
    for href,label,kind in MOBILE_ITEMS:
        cls={'box':'nav-box','group':'nav-box nav-box--active','item':'nav-item'}[kind]
        if href is None:
            out.append(f'    <a class="{cls}" href="index.html">{label}</a>')
        else:
            cur=' aria-current="page"' if href==current else ''
            out.append(f'    <a class="{cls}" href="{href}"{cur}>{label}</a>')
    out.append('  </nav>')
    return "\n".join(out)

PROJECTS = [
    ("neighborhology.html", "Neighborhology – Illustrated Infographics"),
    ("kabai.html", "Kabai Hamangalim – Unity Gameplay"),
    ("missp.html", "Miss P. Home for Peculiar – Title Sequence"),
    ("dia.html", "Dia – UX|UI Diabetes Control Dashboard"),
]


def nav(current, dia_label=None):
    rows = ['    <nav class="snav" aria-label="Main menu">',
            '      <a class="snav__name" href="about.html">Inbal Keller</a>',
            '      <a class="snav__play" href="playground.html">Playground</a>',
            '      <a class="snav__group" href="index.html">Projects</a>']
    for href, label in PROJECTS:
        if href == "dia.html" and dia_label:
            label = dia_label
        cur = ' aria-current="page"' if href == current else ''
        rows.append(f'      <a class="snav__item" href="{href}"{cur}>{label}</a>')
    rows.append('    </nav>')
    return "\n".join(rows)


def desc(items, pad_top=None):
    """items: list of (heading, body_html, extra_class)"""
    style = f' style="--pt: {pad_top}"' if pad_top else ''
    out = [f'    <div class="desc"{style}>']
    for h, body, cls in items:
        out.append(f'      <h2>{h}</h2>')
        c = f' class="{cls}"' if cls else ''
        out.append(f'      <p{c}>{body}</p>')
    out.append('    </div>')
    return "\n".join(out)


def pos(x, y, w, h_total):
    s = f"left:{x / COL * 100:.3f}%;top:{y / h_total * 100:.3f}%"
    if w:
        s += f";width:{w / COL * 100:.3f}%"
    return s


def page(fname, title, theme, sidebar, content):
    html = HEAD.format(title=title, theme=theme, mobile=mobile(fname), meta=META(fname, title))
    proj = fname in ('neighborhology.html', 'kabai.html', 'missp.html', 'dia.html', 'playground.html')
    btn = ('  <button class="nav-close" type="button" aria-expanded="true" aria-label="Close the menu">'
           '<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M15 6l14 14-14 14" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>\n') if proj else ''
    html += '\n<div class="layout">\n  <aside class="sidebar">\n' + sidebar + '\n  </aside>\n' + btn + '\n'
    html += '  <main class="content">\n' + content + '\n  </main>\n</div>\n'
    html += FOOT
    with open(OUT + fname, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", fname)


def img(src, alt, w=1972, h=None):
    hh = f' height="{h}"' if h else ''
    return f'    <img class="block-img" src="images/{src}" alt="{alt}" width="{w}"{hh} loading="lazy">'


# ---------------------------------------------------------------- Neighborhology
page("neighborhology.html", "Neighborhology | Inbal Keller", "theme-neighborhology",
     nav("neighborhology.html") + "\n" + desc([
         ("Tell Me Fast!", "<em>TLV MUNICIPALITY DEMOGRAPHIC ILLUSTRATIONS BOOK</em>", ""),
         ("The Brief", "Illustrate a book.", ""),
         ("What Did I Do?", "An A2-size book + web page presenting a data <br>report on the socio-economic status of the <br>different neighborhoods in TLV.", ""),
         ("Why?", "To raise awareness and express the differences <br>between north &amp; south TLV.", ""),
     ], pad_top=42),
     "\n".join([
         img("neighborhology-1.jpg", "Neighborhology book: the red cover and an illustrated map spread", 1972, 2220),
         "    <div class=\"ncard-wrap\">\n" + img("neighborhology-2.jpg", "Neve Dan map spread with its data card", 1972, 2220) + "\n      <div class=\"ncard\" data-i=\"0\" style=\"left:71.906%; top:3.378%; width:22.566%; height:66.970%\">\n        <img class=\"ncard__img is-on\" src=\"images/ncard-0.webp\" alt=\"Data card: Neve Dan\" width=\"891\" height=\"2977\">\n        <img class=\"ncard__img\" src=\"images/ncard-1.webp\" alt=\"Data card: Neve Sha’anan\" width=\"891\" height=\"2977\" loading=\"lazy\">\n        <img class=\"ncard__img\" src=\"images/ncard-2.webp\" alt=\"Data card: Kochav HaTzafon\" width=\"891\" height=\"2977\" loading=\"lazy\">\n        <img class=\"ncard__img\" src=\"images/ncard-3.webp\" alt=\"Data card: Ramat Aviv\" width=\"891\" height=\"2977\" loading=\"lazy\">\n        <img class=\"ncard__img\" src=\"images/ncard-4.webp\" alt=\"Data card: HaTzafon HaYashan\" width=\"891\" height=\"2977\" loading=\"lazy\">\n        <img class=\"ncard__img\" src=\"images/ncard-5.webp\" alt=\"Data card: Lev Tel Aviv\" width=\"891\" height=\"2977\" loading=\"lazy\">\n        <button class=\"ncard__btn ncard__next\" style=\"left:27.160%; top:91.569%; width:45.342%; height:4.602%\" type=\"button\" aria-label=\"Next neighborhood\"></button>\n        <button class=\"ncard__btn ncard__prev\" style=\"left:30.752%; top:91.569%; width:18.35%; height:4.602%\" type=\"button\" aria-label=\"Previous neighborhood\"><svg viewBox=\"0 0 40 20\" aria-hidden=\"true\"><path d=\"M2 10h36M10 3 2 10l8 7\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"3\" stroke-linejoin=\"miter\"/></svg></button>\n        <button class=\"ncard__btn ncard__fwd\" style=\"left:50.168%; top:91.569%; width:18.35%; height:4.602%\" type=\"button\" aria-label=\"Next neighborhood\"><svg viewBox=\"0 0 40 20\" aria-hidden=\"true\"><path d=\"M2 10h36M10 3 2 10l8 7\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"3\" stroke-linejoin=\"miter\"/></svg></button>\n      </div>\n    </div>",
         '    <div class="nzoom-wrap">',
         img("neighborhology-3.jpg", "Patterned end papers and the back cover with a data card", 1972, 2220),
         """      <button class="nzoom" type="button" data-src="images/nmap-1.jpg" aria-label="View neighborhood map 1 full screen" style="left:0%; top:88.24%; width:25.15%; height:11.76%"></button>
      <button class="nzoom" type="button" data-src="images/nmap-2.jpg" aria-label="View neighborhood map 2 full screen" style="left:25.15%; top:88.24%; width:25.15%; height:11.76%"></button>
      <button class="nzoom" type="button" data-src="images/nmap-3.jpg" aria-label="View neighborhood map 3 full screen" style="left:50.3%; top:88.24%; width:25.16%; height:11.76%"></button>
      <button class="nzoom" type="button" data-src="images/nmap-4.jpg" aria-label="View neighborhood map 4 full screen" style="left:75.46%; top:88.24%; width:24.54%; height:11.76%"></button>""",
         '    </div>',
         '    <div class="nzoom-wrap">',
         img("neighborhology-4.jpg", "Neighborhood map illustrations and inspirations: Tel Aviv parking fines", 1972, 2220),
         """      <button class="nzoom" type="button" data-src="images/nmap-1.jpg" aria-label="View neighborhood map 1 full screen" style="left:0%; top:0%; width:25.15%; height:18.02%"></button>
      <button class="nzoom" type="button" data-src="images/nmap-2.jpg" aria-label="View neighborhood map 2 full screen" style="left:25.15%; top:0%; width:25.15%; height:18.02%"></button>
      <button class="nzoom" type="button" data-src="images/nmap-3.jpg" aria-label="View neighborhood map 3 full screen" style="left:50.3%; top:0%; width:25.16%; height:18.02%"></button>
      <button class="nzoom" type="button" data-src="images/nmap-4.jpg" aria-label="View neighborhood map 4 full screen" style="left:75.46%; top:0%; width:24.54%; height:18.02%"></button>
      <button class="nzoom" type="button" data-src="images/nmap-5.jpg" aria-label="View neighborhood map 5 full screen" style="left:0%; top:18.02%; width:25.15%; height:31.62%"></button>
      <button class="nzoom" type="button" data-src="images/nmap-6.jpg" aria-label="View neighborhood map 6 full screen" style="left:25.15%; top:18.02%; width:25.15%; height:31.62%"></button>
      <button class="nzoom" type="button" data-src="images/nmap-7.jpg" aria-label="View neighborhood map 7 full screen" style="left:50.3%; top:18.02%; width:25.16%; height:31.62%"></button>
      <button class="nzoom" type="button" data-src="images/nmap-8.jpg" aria-label="View neighborhood map 8 full screen" style="left:75.46%; top:18.02%; width:24.54%; height:31.62%"></button>""",
         '    </div>',
         '    <a class="cta" href="https://www.figma.com/proto/G3kKYV2LbLeE2VB62zxJjF/%D7%A9%D7%9B%D7%95%D7%A0%D7%95%D7%9C%D7%95%D7%92%D7%99%D7%94?team_id=1566791894242293013&node-id=1-5&page-id=0%3A1&starting-point-node-id=1%3A5&t=L9UIM557qIdlvFFr-1" target="_blank" rel="noopener" style="--cta-h: 161">Explore Prototype</a>',
         '    <div class="lightbox" role="dialog" aria-modal="true" aria-label="Neighborhood map" hidden>\n      <img class="lightbox__img" alt="Neighborhood map, full screen">\n      <button class="lightbox__x" type="button" aria-label="Close and go back to Neighborhology"><svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M8 8l24 24M32 8L8 32"/></svg></button>\n    </div>',
     ]))

# ---------------------------------------------------------------- Kabai
KH = 887
page("kabai.html", "Kabai Hamangalim | Inbal Keller", "theme-kabai",
     nav("kabai.html") + "\n" + desc([
         ("Tell Me Fast!", "<em>UNITY GAME</em>", ""),
         ("The Brief", "Design &amp; vibe-code a game.", ""),
         ("What Did I Do?", "I created “Kabai Hamangalim”. You are a boy <br>working for “Rashut Hateva Vehaganim”, and you <br>need to put out barbecues &amp; fires.", "tight"),
         ("Why?", "The game is a satirical take on the <br>“ugly Israeli” phenomenon.", "lh-32"),
     ], pad_top=78),
     "\n".join([
         '    <div class="block-video" style="aspect-ratio: 1036 / 626">',
         '      <video src="web-videos/kabai-v2.mp4" poster="images/kabai-poster.jpg" autoplay muted loop playsinline controls></video>',
         '    </div>',
         '    <section class="fbx-section">',
         '      <h3 class="label">FBX</h3>',
         '      <div class="fbx-row">',
         '        <figure class="fbx"><model-viewer src="models/main-character.glb" alt="3D model: the main character in T-pose" camera-controls disable-zoom disable-pan touch-action="pan-y" auto-rotate rotation-per-second="14deg" exposure="0.95" tone-mapping="neutral" camera-orbit="0deg 80deg 105%" interaction-prompt="none" loading="lazy"><div slot="progress-bar"></div></model-viewer></figure>',
         '        <figure class="fbx"><model-viewer src="models/gothic-girl.glb" alt="3D model: gothic girl" camera-controls disable-zoom disable-pan touch-action="pan-y" auto-rotate rotation-per-second="14deg" exposure="0.95" tone-mapping="neutral" camera-orbit="0deg 80deg 105%" interaction-prompt="none" loading="lazy"><div slot="progress-bar"></div></model-viewer></figure>',
         '        <figure class="fbx"><model-viewer src="models/man-with-beef.glb" alt="3D model: man with beef" camera-controls disable-zoom disable-pan touch-action="pan-y" auto-rotate rotation-per-second="14deg" exposure="0.95" tone-mapping="neutral" camera-orbit="0deg 80deg 105%" interaction-prompt="none" loading="lazy"><div slot="progress-bar"></div></model-viewer></figure>',
         '        <figure class="fbx"><model-viewer src="models/wave-man.glb" alt="3D model: waving man" camera-controls disable-zoom disable-pan touch-action="pan-y" auto-rotate rotation-per-second="14deg" exposure="0.95" tone-mapping="neutral" camera-orbit="0deg 80deg 105%" interaction-prompt="none" loading="lazy"><div slot="progress-bar"></div></model-viewer></figure>',
         '        <figure class="fbx"><model-viewer src="models/woman.glb" alt="3D model: woman" camera-controls disable-zoom disable-pan touch-action="pan-y" auto-rotate rotation-per-second="14deg" exposure="0.95" tone-mapping="neutral" camera-orbit="0deg 80deg 105%" interaction-prompt="none" loading="lazy"><div slot="progress-bar"></div></model-viewer></figure>',
         '        <figure class="fbx"><model-viewer src="models/keter-chair.glb" alt="3D model: Keter plastic chair" camera-controls disable-zoom disable-pan touch-action="pan-y" auto-rotate rotation-per-second="14deg" exposure="0.95" tone-mapping="neutral" camera-orbit="30deg 72deg 115%" interaction-prompt="none" loading="lazy"><div slot="progress-bar"></div></model-viewer></figure>',
         '        <figure class="fbx"><model-viewer src="models/fire-extinguisher.glb" alt="3D model: fire extinguisher" camera-controls disable-zoom disable-pan touch-action="pan-y" auto-rotate rotation-per-second="14deg" exposure="0.95" tone-mapping="neutral" camera-orbit="30deg 75deg 110%" interaction-prompt="none" loading="lazy"><div slot="progress-bar"></div></model-viewer></figure>',
         '      </div>',
         '    </section>',
         img("kabai-font.jpg", "Atlas font specimen", 1972, 646),
         img("kabai-inspirations-v2.jpg", "Inspirations: the ugly Israeli phenomenon, Hadera National Reserve", 1972, 817),
         '    <script type="module" src="vendor/model-viewer.min.js"></script>',
     ]))

# ---------------------------------------------------------------- Miss P
MH = 1890
page("missp.html", "Miss P. Home for Peculiar | Inbal Keller", "theme-missp",
     nav("missp.html") + "\n" + desc([
         ("The Brief", "Create a title sequence for a book.", ""),
         ("What Did I Do?", "Miss Peregrine’s Home for Peculiar Children, <br>by Ransom Riggs.", "tight"),
         ("What Is It About?", "Children with peculiar abilities hide from <br>monsters in a 1940 time loop. Behind the <br>fantasy is the Holocaust, and the way children <br>use escapism to survive.", "lh-32"),
         ("Tell Me Fast!", "Escapism | Vintage | Mysterious", ""),
     ], pad_top=42),
     "\n".join([
         '    <div class="block-video" style="--cta-h: 555">',
         '      <video src="web-videos/missp.mp4" poster="images/missp-poster-frame.jpg" autoplay muted loop playsinline controls></video>',
         '    </div>',
         f'    <section class="canvas missp-black" style="aspect-ratio: 986 / {MH}">',
         f'      <h3 class="t-h" style="{pos(79.5, 120, 0, MH)}">Typography</h3>',
         f'      <p class="t-b" style="{pos(79.5, 159.5, 300, MH)}">The lettering is taken from a <br>poster from the ghetto, from the <br>Yad Vashem website. <br>The fonts David &amp; The Basics <br>Mono by The Gilda are also used.</p>',
         f'      <img src="images/missp-poster.jpg" alt="Poster from the ghetto (Yad Vashem) used as the lettering source" width="1032" height="620" loading="lazy" style="{pos(386, 89, 516, MH)}">',
         f'      <h3 class="t-h" style="{pos(80, 467.5, 0, MH)}">Sound</h3>',
         f'      <p class="t-b" style="{pos(80, 510, 300, MH)}">“Rivolta” by Polo &amp; Pan</p>',
         f'      <h3 class="t-h" style="{pos(80.5, 605, 0, MH)}">Images</h3>',
         f'      <p class="t-r" style="{pos(79, 646, 560, MH)}">The book’s vintage postcards (from the author’s own collection) | Yad Vashem archives | AI</p>',
         f'      <img src="images/missp-postcards.jpg" alt="Three vintage postcards from the book" width="1368" height="680" loading="lazy" style="{pos(220, 793, 684, MH)}">',
         f'      <h3 class="t-h" style="{pos(78.5, 1178.5, 0, MH)}">Storyboard</h3>',
         f'      <img src="images/missp-storyboard.jpg" alt="Storyboard: sixteen frames of the title sequence" width="1900" height="1136" loading="lazy" style="{pos(18, 1253, 950, MH)}">',
         '    </section>',
         '    <a class="cta" href="web-videos/missp.mp4" target="_blank" rel="noopener" style="--cta-bg: #0004FF; --cta-h: 152">Watch Now</a>',
     ]))



# Dia on phones: the same images cut into bands and cropped to their content
# (made by dia_mobile.py) so the text shows bigger. Videos keep their place.
import json as _json
_DM = _json.load(open('/home/claude/dia_mobile.json'))
_DIA_VIDS = {
    '1': [((455.3,1858.0,335.9,597.1),"dia-app-workout.mp4","Dia app screen recording"),
          ((820.1,1664.4,337.8,600.5),"dia-app-signup.mp4","Dia app screen recording"),
          ((1193.6,1833.8,348.7,620.0),"dia-app-nudge.mp4","Dia app screen recording")],
    '7': [((651.0,976.0,197.0,352.0),"dia-insulin-1.mp4","Insulin loading animation"),
          ((873.0,976.0,197.0,352.0),"dia-insulin-2.mp4","Insulin loading animation")],
}
def dia_mobile(alts):
    out = ['    <div class="dia-mob">']
    for k in map(str, range(1, 9)):
        for n, p in enumerate(_DM[k]):
            vids = [v for v in _DIA_VIDS.get(k, []) if p['y0'] <= v[0][1] < p['y1']]
            tag = f'      <img class="block-img" src="images/{p["file"]}" alt="{alts[int(k)-1] if n == 0 else ""}" width="{p["w"]}" height="{p["h"]}" loading="lazy">'
            if vids:
                out.append('      <div class="dia-anim">')
                out.append('  ' + tag)
                for (x, y, w, h), f, a in vids:
                    st = f'left:{(x-p["x0"])/p["w"]*100:.3f}%; top:{(y-p["y0"])/p["h"]*100:.3f}%; width:{w/p["w"]*100:.3f}%; height:{h/p["h"]*100:.3f}%'
                    out.append(f'        <video class="dia-anim__v" style="{st}" data-src="web-videos/{f}" muted loop playsinline aria-label="{a}"></video>')
                out.append('      </div>')
            else:
                out.append(tag)
    out.append('    </div>')
    return "\n".join(out)

# ---------------------------------------------------------------- DIA
DIA_ALTS = ['Hi! Meet Dia, a personal diabetes control dashboard. Dia is an app, created for keeping track of diabetes. PLZ explain: what is diabetes?', 'PLZ explain: what is diabetes? What are the main problems diabeaters face?', 'So, what did we do? An app that makes controlling diabetes easier. Why choose Dia?', 'Personas: Rami and Adam', 'UX: wireframes and user flow', 'Our main design goal: make it simple and calm the user. Design System: palette and typography', 'UI and buttons, sugar level indication avatars, micro animations', 'Learning from users: we let Rami try Dia, and these were his struggles. We fixed it for Rami.']
page("dia.html", "Dia – UX|UI Diabetes Control Dashboard | Inbal Keller", "theme-dia",
     nav("dia.html") + "\n" + desc([
         ("The Brief", "Design a UX|UI dashboard.", ""),
         ("What Did I Do?", "A personal diabetes control dashboard.", "tight"),
         ("What Is It About?", "How to keep track of your diabetes.", ""),
     ], pad_top=40),
     "\n".join([
         '    <div class="dia-desk">',
         '    <div class="dia-anim">',
         img("dia-1.jpg", "Hi! Meet Dia, a personal diabetes control dashboard. Dia is an app, created for keeping track of diabetes. PLZ explain: what is diabetes?", 1972, 3909),
         '      <video class="dia-anim__v" style="left:23.090%; top:47.529%; width:17.033%; height:15.276%" data-src="web-videos/dia-app-workout.mp4" muted loop playsinline aria-label="Dia app screen recording"></video>',
         '      <video class="dia-anim__v" style="left:41.588%; top:42.578%; width:17.129%; height:15.362%" data-src="web-videos/dia-app-signup.mp4" muted loop playsinline aria-label="Dia app screen recording"></video>',
         '      <video class="dia-anim__v" style="left:60.529%; top:46.912%; width:17.684%; height:15.860%" data-src="web-videos/dia-app-nudge.mp4" muted loop playsinline aria-label="Dia app screen recording"></video>',
         '    </div>',
         img("dia-2.jpg", "PLZ explain: what is diabetes? What are the main problems diabeaters face?", 1972, 2400),
         img("dia-3.jpg", "So, what did we do? An app that makes controlling diabetes easier. Why choose Dia?", 1972, 2400),
         img("dia-4.jpg", "Personas: Rami and Adam", 1972, 2400),
         img("dia-5.jpg", "UX: wireframes and user flow", 1972, 2400),
         img("dia-6.jpg", "Our main design goal: make it simple and calm the user. Design System: palette and typography", 1972, 2400),
         '    <div class="dia-anim">',
         img("dia-7.jpg", "UI and buttons, sugar level indication avatars, micro animations", 1972, 2400),
         '      <video class="dia-anim__v" style="left:33.012%; top:40.667%; width:9.990%; height:14.667%" data-src="web-videos/dia-insulin-1.mp4" muted loop playsinline aria-label="Insulin loading animation"></video>',
         '      <video class="dia-anim__v" style="left:44.270%; top:40.667%; width:9.990%; height:14.667%" data-src="web-videos/dia-insulin-2.mp4" muted loop playsinline aria-label="Insulin loading animation"></video>',
         '    </div>',
         img("dia-8.jpg", "Learning from users: we let Rami try Dia, and these were his struggles. We fixed it for Rami.", 1972, 1590),
         '    </div>',
         dia_mobile(DIA_ALTS),
         '    <a class="cta cta--sticky" href="https://www.figma.com/proto/93YAOm9JhSEP0Y9UNeOsVW/spare?node-id=1-1537&p=f&m=draw&scaling=min-zoom&content-scaling=fixed&starting-point-node-id=1%3A1544&page-id=0%3A1&t=neK9enmEMz6qvxAW-1" target="_blank" rel="noopener" style="--cta-fg: #F0DDFF; --cta-h: 134">Skip To Prototype</a>',
     ]))

# ---------------------------------------------------------------- Playground
pg_side = """    <div class="pg-side__video crop crop--bottom" style="--w:100%; background-image:url(images/playground-pottery-poster.jpg)">
      <video src="web-videos/pottery.mp4" autoplay muted loop playsinline></video>
    </div>
    <nav class="snav" aria-label="Main menu">
      <a class="snav__row" href="about.html">Inbal Keller</a>
      <span class="snav__current" aria-current="page">Playground</span>
      <a class="snav__row" href="index.html">Projects</a>
    </nav>"""
page("playground.html", "Playground | Inbal Keller", "theme-playground", pg_side,
     "\n".join([
         '    <!-- Playground: every picture & video is its own layer, placed as in Figma.',
         '         Each section (flowers, dog, frame of photos) stops and the next one slides over it. -->',
         '    <div class="pg-layers">',
         '      <section class="pg-group pg-group--stick" style="--gh:1389.2; --gx:600" aria-label="flowers">',
         '        <div class="pg-bg" style="--bh:1389.2">',
         '        <div class="pgl" style="--x:0; --y:-24.5; --w:987; --h:1416.7"><img class="pgl__in" src="images/pg-floral.jpg" alt="Floral drawing" width="1988" height="2852"></div>',
         '        <div class="pgl" style="--x:376.5; --y:222.5; --w:303; --h:512"><img class="pgl__in" src="images/pg-oboe-girl.png" alt="Illustration of Inbal playing the oboe" width="606" height="1024"></div>',
         '        </div>',
         '        <div class="pgl" style="--x:81; --y:858; --w:848; --h:478"><div class="pgl__in pgl__video"><video src="web-videos/interceptor.mp4" poster="images/playground-interceptor-poster.jpg" autoplay muted loop playsinline controls></video></div></div>',
         '      </section>',
         '      <section class="pg-group pg-group--stick" style="--gh:1002.2; --gx:450" aria-label="dog">',
         '        <div class="pg-bg" style="--bh:1002.2"><div class="pgl" style="--x:0; --y:0.0; --w:987; --h:1002.2"><img class="pgl__in" src="images/pg-dog.jpg" alt="Dog painting" width="779" height="791" loading="lazy"></div></div>',
         '        <div class="pgl" style="--x:115; --y:377.8; --w:776; --h:435"><div class="pgl__in pgl__video"><video src="web-videos/stutter.mp4" poster="images/playground-stutter-poster.jpg" autoplay muted loop playsinline controls></video></div></div>',
         '      </section>',
         '      <section class="pg-group" style="--gh:1226.6" aria-label="postcards">',
         '        <div class="pgl" style="--x:0; --y:42.6; --w:219; --h:280.8"><img class="pgl__in" src="images/pg-card-1.jpg" alt="Watercolor postcard" width="438" height="562" loading="lazy"></div>',
         '        <div class="pgl" style="--x:522; --y:56.6; --w:221; --h:283.4"><img class="pgl__in" src="images/pg-card-3.jpg" alt="Watercolor postcard: the road to the Arava" width="442" height="567" loading="lazy"></div>',
         '        <div class="pgl" style="--x:260; --y:104.6; --w:200; --h:285.3"><img class="pgl__in" src="images/pg-card-2.jpg" alt="Watercolor postcard: date plantations" width="400" height="571" loading="lazy"></div>',
         '        <div class="pgl" style="--x:682; --y:388.6; --w:248; --h:327.2"><img class="pgl__in" src="images/pg-card-6.jpg" alt="Watercolor postcard: thirsty farmer" width="496" height="654" loading="lazy"></div>',
         '        <div class="pgl" style="--x:24; --y:410.6; --w:217; --h:286.5"><img class="pgl__in" src="images/pg-card-4.jpg" alt="Watercolor postcard" width="434" height="573" loading="lazy"></div>',
         '        <div class="pgl" style="--x:410; --y:456.6; --w:222; --h:265.3"><img class="pgl__in" src="images/pg-card-5.jpg" alt="Watercolor postcard: military service" width="444" height="531" loading="lazy"></div>',
         '        <div class="pgl" style="--x:210; --y:781.6; --w:268; --h:385.1"><img class="pgl__in" src="images/pg-pencil.jpg" alt="Pencil drawing: working in a tomato greenhouse" width="536" height="770" loading="lazy"></div>',
         '        <div class="pgl" style="--x:543; --y:782.6; --w:222.5; --h:299"><img class="pgl__in" src="images/pg-card-7.jpg" alt="Watercolor painting of a hillside path" width="445" height="598" loading="lazy"></div>',
         '      </section>',
         '      <section class="pg-group" style="--gh:1037" aria-label="Crave">',
         '        <div class="pgl" style="--x:0; --y:0; --w:987; --h:1037"><img class="pgl__in" src="images/pg-crave.jpg" alt="Crave: illustrated dessert cups packaging, with a kitchen sketch and a cookie character" width="1974" height="2074" loading="lazy"></div>',
         '        <div class="pgl" style="--x:5; --y:485; --w:982; --h:552"><div class="pgl__in pgl__video"><video src="web-videos/crave-opening.mp4" autoplay muted loop playsinline aria-label="Crave: the cookie character in the kitchen"></video></div></div>',
         '        <div class="pgl" style="--x:0; --y:483; --w:987; --h:142; pointer-events:none"><img class="pgl__in" src="images/pg-crave-cups.png" alt="" width="1974" height="284" loading="lazy"></div>',
         '      </section>',
         '    </div>',
     ]))

# ---------------------------------------------------------------- About
about = HEAD.format(title="Inbal Keller | About", theme="theme-about", mobile=mobile("about.html"), meta=META("about.html", "Inbal Keller | About")) + """
<div class="layout">
  <aside class="sidebar">
    <div class="pg-side__video crop crop--bottom" style="--w:100%; background-image:url(images/playground-pottery-poster.jpg)">
      <video src="web-videos/pottery.mp4" autoplay muted loop playsinline></video>
    </div>
    <nav class="snav" aria-label="Main menu">
      <span class="snav__current" aria-current="page">Inbal Keller</span>
      <a class="snav__row" href="playground.html">Playground</a>
      <a class="snav__row" href="index.html">Projects</a>
    </nav>
    <div class="about-text">
      <p><b>I am Inbal</b>, a 4th-year Visual Communication <br>Design student.</p>
      <p>I have been playing the oboe since I was 9, and I <br>was part of the Israel Young Philharmonic <br>Orchestra for 4 years during high school. My <br>extra skills are illustrating, sewing &amp; <br>ceramics. <b>I’m a crafty person!</b></p>
      <p><b>I believe teamwork is a must-have skill.</b> <br>I am always up for researching &amp; learning new <br>things. I like yoga.</p>
    </div>
  </aside>

  <main class="content about">
    <img class="about-girl" src="images/about-oboe-girl.jpg" alt="Illustration of Inbal playing the oboe" width="260" height="560">
    <!-- Photos scroll up and stick near the top, stacking (Figma prototype) -->
    <div class="ph" style="--top:197; --left:244; --w:459"><img src="images/about-portrait.jpg" alt="Portrait of Inbal Keller" width="918" height="1297"></div>
    <div class="ph" style="--top:910; --left:0; --w:459"><img src="images/about-oboe-photo.jpg" alt="Inbal with her oboe" width="918" height="1380" loading="lazy"></div>
    <div class="ph" style="--top:1622; --left:444; --w:459"><img src="images/about-studio.jpg" alt="Inbal photographing in the studio" width="918" height="1210" loading="lazy"></div>
    <div class="ph" style="--top:2283; --left:244; --w:459"><img src="images/about-child-full.jpg" alt="Inbal as a child" width="918" height="1454" loading="lazy"></div>
  </main>
</div>
""" + FOOT
with open(OUT + "about.html", "w", encoding="utf-8") as f:
    f.write(about)
print("wrote about.html")
