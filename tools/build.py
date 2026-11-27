#!/usr/bin/env python3
"""Generates the static Hooks Permanent Lighting (HPL) site into the repo root.

Run from anywhere:  python3 tools/build.py
Edit SETTINGS below (phone, email, Jobber form) and page copy in this file, then
re-run and commit the generated HTML. GitHub Pages serves the repo root; there is
no other build step.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# ----------------------------------------------------------------------------
# SETTINGS  (edit these)
# ----------------------------------------------------------------------------
SITE = "https://www.hookspermanentlighting.com"
NAME = "Hooks Permanent Lighting"
PARENT_URL = "https://www.hookspropertyservices.com"   # cross-advertising target
PARENT_NAME = "Hooks Property Services"

# Leave PHONE / EMAIL empty to hide them everywhere (quote form only).
PHONE_DISPLAY = "929-270-8504"
EMAIL = ""                  # leave blank: the Email option links to the quote request page instead
HIC_NUMBER = "PA235962"     # PA Home Improvement Contractor registration (shown in footer)
PHONE_TEL = "".join(c for c in PHONE_DISPLAY if c.isdigit())

SERVICE_AREA = "Lancaster, PA"

# Jobber "Work Request" embed (Jobber > Settings > Work Request Settings > Embed).
# Same form the HPS permanent-lighting page uses today.
JOBBER_ID = "5e6214d9-5ba9-47c7-82db-7aa4a62b9021-5330346"
JOBBER_FORM = ("https://clienthub.getjobber.com/client_hubs/5e6214d9-5ba9-47c7-82db-7aa4a62b9021/"
               "public/work_request/embedded_work_request_form?form_id=5330346")

# ----------------------------------------------------------------------------
NAV = [("", "Home"), ("permanent-lighting/", "Permanent Lighting"),
       ("about-us/", "About Us"), ("contact-us/", "Contact Us")]


def jobber_embed():
    return (
        '<div class="jobber-form"><div id="%s"></div>'
        '<link rel="stylesheet" href="https://d3ey4dbjkt2f6s.cloudfront.net/assets/external/work_request_embed.css" media="screen" />'
        '<script src="https://d3ey4dbjkt2f6s.cloudfront.net/assets/static_link/work_request_embed_snippet.js" '
        'clienthub_id="%s" form_url="%s"></script></div>' % (JOBBER_ID, JOBBER_ID, JOBBER_FORM)
    )


def brand(rel):
    return ('<a class="brand" href="%s" aria-label="%s home"><img src="%sassets/logo.png" alt="%s logo" '
            'width="96" height="100"></a>' % (rel or "./", NAME, rel, NAME))


def head(title, desc, path, rel, image="assets/permanent-lighting.jpg"):
    url = SITE + "/" + path
    ld = {"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness",
          "name": NAME, "url": SITE, "image": SITE + "/" + image,
          "areaServed": [SERVICE_AREA],
          "description": "Permanent roofline lighting installation in Lancaster, PA."}
    if PHONE_TEL:
        ld["telephone"] = "+1-" + PHONE_DISPLAY
    if EMAIL:
        ld["email"] = EMAIL
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/x-icon" href="{rel}favicon.ico">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/{image}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}assets/style.css">
<script type="application/ld+json">{json.dumps(ld)}</script>
</head>
"""


def top(rel, current, home=False):
    if PHONE_TEL:
        ann = f'<a href="tel:{PHONE_TEL}">Call Now: {PHONE_DISPLAY}</a>'
    else:
        ann = f'<a href="{rel}contact-us/">Free Permanent Lighting Quotes &mdash; Request Yours Today</a>'
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{rel}{p}"{cur if p == current else ""}>{label}</a>' for p, label in NAV)
    return f"""<body class="{'home' if home else 'inner'}">
<div class="announce" id="announce">{ann}<button type="button" aria-label="Close Announcement" onclick="document.getElementById('announce').remove()">&times;</button></div>
<header class="site-header">
  {brand(rel)}
  <button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false" onclick="var n=document.getElementById('nav');var o=n.classList.toggle('open');this.setAttribute('aria-expanded',o)">&#9776;</button>
  <nav id="nav">{links}<a class="btn btn-sm" href="{rel}contact-us/">Get A Quote</a></nav>
</header>
<main>
"""


def contact_block(rel):
    out = ""
    if PHONE_TEL:
        out += f'<p class="ic"><img src="{rel}assets/phone-icon.png" alt="" width="28" height="28"><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>'
    out += f'<p class="ic"><img src="{rel}assets/email-icon.png" alt="" width="28" height="28"><a href="{rel}contact-us/">Email Us</a></p>'
    return out


def bottom(rel):
    explore = "".join(f'<p><a href="{rel}{p}">{l}</a></p>' for p, l in NAV)
    return f"""
</main>
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div>{brand(rel)}</div>
    <div><h4>Contact</h4>{contact_block(rel)}</div>
    <div><h4>Service Area</h4><p>{SERVICE_AREA}</p></div>
    <div><h4>Explore</h4>{explore}
      <p><a href="{PARENT_URL}/christmas-lights/">Christmas Lights</a></p></div>
  </div>
  <p class="copy">&copy; <span id="yr">2026</span> {NAME}. All rights reserved.<br>PA Home Improvement Contractor Registration # {HIC_NUMBER}</p>
</footer>
<script>document.getElementById('yr').textContent=new Date().getFullYear();</script>

</body>
</html>
"""


def cta(rel, heading="Get Started Today", text=None):
    text = text or ("Ready for year-round curb appeal without the ladder? Request a free permanent lighting quote "
                    "and we&rsquo;ll plan the layout for your roofline.")
    call = (f'<a class="btn btn-ghost" href="tel:{PHONE_TEL}">Call Now: {PHONE_DISPLAY}</a>' if PHONE_TEL else "")
    return f"""<section class="cta" style="background-image:linear-gradient(rgba(0,24,56,.72),rgba(0,24,56,.72)),url('{rel}assets/lakeside-lighting.jpg')">
  <div class="wrap center"><h2>{heading}</h2><p>{text}</p>
  <div class="btns" style="justify-content:center;margin-top:10px"><a class="btn" href="{rel}contact-us/">Get a Free Quote</a>{call}</div></div></section>"""


def xpromo(rel):
    return f"""<section class="xpromo gray"><div class="wrap">
  <div><h3>Need window cleaning or Christmas lights too?</h3>
  <p>{PARENT_NAME} offers professional window cleaning and Christmas light installation in Lancaster, PA.</p></div>
  <a class="btn" href="{PARENT_URL}/">Visit {PARENT_NAME}</a></div></section>"""


def trimlight(rel, variant):
    """Trimlight brand / authorized-dealer / lifetime-warranty section.
    variant: "home" (navy, lead photo), "pl" (light, patio photo), "about" (navy, dealer story).
    Logos and badge come from the Trimlight marketing library (assets/trimlight-*)."""
    dealer_w = (f'<img class="tl-logo" src="{rel}assets/trimlight-authorized-dealer-white.png" '
                'alt="Trimlight Authorized Dealer logo" width="900" height="480" loading="lazy">')
    dealer_b = (f'<img class="tl-logo" src="{rel}assets/trimlight-authorized-dealer-black.png" '
                'alt="Trimlight Authorized Dealer logo" width="900" height="447" loading="lazy">')
    badge = (f'<img class="tl-badge" src="{rel}assets/trimlight-lifetime-warranty-badge.png" '
             'alt="Trimlight lifetime product warranty badge" width="520" height="561" loading="lazy">')
    note = ('<p class="tl-note">Warranty terms and coverage are provided by Trimlight. '
            'Ask us for the details with your free quote.</p>')
    if variant == "home":
        return f"""<section class="tl navy"><div class="wrap two">
  <div class="tl-copy">{dealer_w}
  <p class="eyebrow">Our Brand</p>
  <h2>Quality You Can Count On: <span class="y">Trimlight</span></h2>
  <p>Hooks Permanent Lighting is an authorized Trimlight dealer serving Lancaster County. We install Trimlight, an established permanent lighting brand, and Trimlight offers a lifetime product warranty.</p>
  <ul><li>Authorized Trimlight dealer in Lancaster County</li><li>Lifetime product warranty from Trimlight</li><li>App-controlled colors, patterns, and schedules</li><li>Low-profile track that blends into your roofline</li></ul>
  {note}
  <p><a class="btn" href="{rel}permanent-lighting/">See How Permanent Lighting Works</a></p></div>
  <div class="tl-media"><img class="photo" src="{rel}assets/trimlight-home-dusk.jpg" alt="Home with Trimlight permanent roofline lighting at dusk" width="1600" height="1066" loading="lazy">{badge}</div>
</div></section>"""
    if variant == "pl":
        return f"""<section class="tl light gray"><div class="wrap two">
  <div class="tl-media"><img class="photo" src="{rel}assets/trimlight-patio-pool.jpg" alt="Backyard patio and pool with Trimlight permanent lighting along the roofline" width="1400" height="980" loading="lazy">{badge}</div>
  <div class="tl-copy">{dealer_b}
  <h2>Installed with <span class="hl">Trimlight</span></h2>
  <p>We are an authorized Trimlight dealer, so your permanent lighting is a quality brand-name system installed locally in Lancaster County by Hooks Permanent Lighting.</p>
  <ul><li>Trimlight lifetime product warranty</li><li>Colors, patterns, and schedules from your phone</li><li>Clean, low-profile track along your roofline</li></ul>
  {note}
  <p><a class="btn" href="{rel}contact-us/">Get a Free Quote</a></p></div>
</div></section>"""
    return f"""<section class="tl navy"><div class="wrap two">
  <div class="tl-copy"><p class="eyebrow">Authorized Dealer</p>
  <h2>Your Lancaster County <span class="y">Trimlight</span> Dealer</h2>
  <p>Hooks Permanent Lighting is an authorized Trimlight dealer serving Lancaster County, PA. That means we bring a quality permanent lighting brand to your home, installed by a local team that takes ownership of every job.</p>
  <p>Trimlight backs its product with a lifetime product warranty, and you get a local company you can call for your install.</p>
  {note}
  <p><a class="btn" href="{rel}permanent-lighting/">Explore Permanent Lighting</a></p></div>
  <div class="tl-badges">{dealer_w}{badge}</div>
</div></section>"""


def page_title(h):
    return f'<section class="page-title navy"><div class="wrap"><h1 class="y">{h}</h1></div></section>'


def quote_section(rel, h2="Request a Free Permanent Lighting Quote"):
    return f"""<section class="gray pad" id="quote"><div class="wrap narrow"><h2 class="center">{h2}</h2>
  <p class="center">Tell us about your home and we&rsquo;ll get back to you with a quote.</p>{jobber_embed()}</div></section>"""


def write(path, html):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html)


# ----------------------------------------------------------------------------
# Shared copy
# ----------------------------------------------------------------------------
FEATURES_UL = ("<ul><li>Low-profile roofline track</li><li>App-controlled colors and patterns</li>"
               "<li>Holiday and everyday lighting</li><li>Residential and commercial installs</li></ul>")
STEPS = [("Request a free quote", "Tell us about your home online."),
         ("We plan the layout", "We map out the lighting for your roofline."),
         ("We install", "A clean, careful install of the low-profile track and lights."),
         ("You take control", "Set colors, brightness, and schedules from your phone.")]

# ----------------------------------------------------------------------------
# HOME
# ----------------------------------------------------------------------------
def home():
    rel = ""
    title = f"Permanent Lighting Installation Lancaster PA | {NAME}"
    desc = ("Authorized Trimlight dealer in Lancaster, PA. Permanent roofline lighting with app-controlled colors "
            "and schedules, backed by the Trimlight lifetime product warranty. Request a free quote.")
    steps = "".join(f"<li><strong>{a}</strong>{b}</li>" for a, b in STEPS)
    feats = [("Low-Profile Roofline Track", "A clean, low-profile track mounted along your roofline that blends into your home&rsquo;s look."),
             ("App-Controlled Colors", "Change colors, brightness, and patterns from your phone in seconds."),
             ("Holiday &amp; Everyday Lighting", "Light up for the holidays, game days, or simple warm-white accent lighting any night."),
             ("Homes &amp; Businesses", "Residential and commercial installs across Lancaster, PA.")]
    feat_html = "".join(f"<article><h3>{a}</h3><p>{b}</p></article>" for a, b in feats)
    call = (f'<a class="btn btn-ghost" href="tel:{PHONE_TEL}">Call Now</a>' if PHONE_TEL else
            '<a class="btn btn-ghost" href="permanent-lighting/">How It Works</a>')
    faqs = [
        ("What is permanent lighting?", "Permanent lighting is a low-profile track mounted along your roofline with programmable LED lights. You control colors, brightness, and schedules from your phone, so there&rsquo;s no hanging or taking down lights each season."),
        ("How do I get started?", "Tap Get A Quote and tell us about your home. We&rsquo;ll follow up with a free quote and plan the layout for your roofline."),
        ("Can I change the colors for different holidays?", "Yes. You can switch colors, patterns, and brightness any time from your phone, and set schedules for holidays, game days, or everyday accent lighting."),
        ("Do you install on businesses too?", "Yes. We install permanent lighting for both homes and commercial properties in Lancaster, PA."),
        ("What&rsquo;s your pricing model?", "Pricing depends on the length of your roofline and the layout of your lighting. Every quote is free, with no obligation."),
    ]
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    html = head(title, desc, "", rel) + top(rel, "", home=True) + f"""
<section class="hero" style="background-image:linear-gradient(90deg,rgba(0,24,56,.88) 0%,rgba(0,24,56,.55) 55%,rgba(0,24,56,.15) 100%),url('assets/permanent-lighting.jpg')">
  <div class="wrap"><h1><span class="y">Year-Round Permanent Lighting</span> in Lancaster, PA</h1>
  <p>Low-profile roofline lighting you control from your phone. Holidays, game days, or everyday curb appeal &mdash; with no more ladders and no more takedown.</p>
  <div class="btns"><a class="btn" href="contact-us/">Get a Free Quote</a>{call}</div></div>
</section>

<section class="about wrap two">
  <div class="frame"><img src="assets/lakeside-lighting.jpg" alt="Lakeside home with permanent roofline lighting at dusk" width="540" height="360"></div>
  <div><p class="eyebrow">About Us</p><h2>Hooks Permanent <span class="hl">Lighting</span></h2>
  <p>Hooks Permanent Lighting designs and installs permanent roofline lighting for homes and businesses in Lancaster, PA. We bring care and attention to detail to every install.</p>
  <p>Every home is different, so we plan the layout around your roofline, install a clean low-profile track, and set you up to control it all from your phone. The result is lighting that looks great on day one and every night after.</p>
  <p><a class="btn" href="contact-us/">Get A Free Quote</a></p></div>
</section>

<section class="services navy"><div class="wrap">
  <h2 class="center y">Permanent Lighting for Every Season</h2>
  <div class="features">{feat_html}</div></div></section>

<section class="why gray"><div class="wrap two">
  <div><h2>Why Homeowners Choose <span class="hl">Permanent Lighting</span></h2>
  <p>Hanging lights every year is a chore. Permanent lighting gives you a polished look all year and the freedom to change it whenever you like.</p>
  <ul><li>No more hanging and taking down lights every year</li><li>Custom layout planned for your roofline</li><li>Colors, brightness, and schedules from your phone</li><li>Residential and commercial installs</li><li>Free, no-obligation quotes</li><li>Locally owned in Lancaster, PA</li></ul></div>
  <div class="collage"><img class="big" src="assets/permanent-lighting.jpg" alt="Home with permanent roofline lighting at night" width="500" height="375" loading="lazy"><img class="small" src="assets/lakeside-lighting.jpg" alt="" width="300" height="200" loading="lazy"></div>
</div></section>

{trimlight(rel, "home")}

<section class="pad"><div class="wrap"><h2 class="center">How It Works</h2><ol class="steps">{steps}</ol>
  <p class="center" style="margin-top:50px"><a class="btn" href="contact-us/">Get a Free Quote</a></p></div></section>

<section class="faq gray"><div class="wrap narrow"><h2 class="center">Frequently Asked Questions</h2>
  <p class="center">Still have questions? Take a look at the FAQ or send us a quote request anytime.</p>{faq_html}</div></section>

{xpromo(rel)}
{cta(rel)}
""" + bottom(rel)
    write("index.html", html)


# ----------------------------------------------------------------------------
# PERMANENT LIGHTING (matches the layout of the HPS page)
# ----------------------------------------------------------------------------
def pl_page():
    rel = "../"
    title = f"Permanent Lighting Installation | Lancaster, PA — {NAME}"
    desc = ("Permanent roofline lighting in Lancaster, PA. App-controlled colors and schedules for holidays, game "
            "days, and everyday curb appeal. Request a free quote.")
    html = head(title, desc, "permanent-lighting/", rel) + top(rel, "permanent-lighting/") + f"""
{page_title("Permanent Lighting")}
<section class="wrap two pad">
  <div><h2>Permanent Lighting for Every Season</h2>
  <p>Permanent lighting gives your home year-round curb appeal with a low-profile track system mounted along your roofline. Change colors, brightness, and schedules from your phone for holidays, game days, or everyday accent lighting.</p>
  <p>No more hanging and taking down lights every year. Hooks Permanent Lighting installs permanent lighting for homes and businesses in Lancaster, PA with a clean, careful install you can enjoy for years.</p>
  <h4>Permanent Lighting Features</h4>
  {FEATURES_UL}
  <h4>How It Works:</h4>
  <ol><li>Request a free quote</li><li>We plan the layout for your roofline</li><li>We install the low-profile track and lights</li><li>You control colors and schedules from your phone</li></ol></div>
  <div><img class="photo" src="../assets/permanent-lighting.jpg" alt="Permanent roofline lighting" loading="lazy"><img class="photo" style="margin-top:20px" src="../assets/lakeside-lighting.jpg" alt="Lakeside home with permanent lighting" loading="lazy"></div>
</section>
{trimlight(rel, "pl")}
{quote_section(rel)}
{xpromo(rel)}
{cta(rel, text="Permanent lighting is installed and serviced by Hooks Permanent Lighting. Reliable local service you can trust.")}
""" + bottom(rel)
    write("permanent-lighting/index.html", html)


# ----------------------------------------------------------------------------
# ABOUT
# ----------------------------------------------------------------------------
def about():
    rel = "../"
    title = f"About Us | {NAME} — Lancaster, PA"
    desc = ("Hooks Permanent Lighting is a locally owned Lancaster, PA company installing permanent roofline "
            "lighting.")
    html = head(title, desc, "about-us/", rel) + top(rel, "about-us/") + f"""
{page_title("About Us")}
<section class="wrap two pad">
  <div><h2>Locally Owned, Carefully Installed</h2>
  <p>Hooks Permanent Lighting is a locally owned company that designs and installs permanent roofline lighting for homes and businesses in Lancaster, PA.</p>
  <p>We started Hooks Permanent Lighting because we saw how much homeowners love great lighting &mdash; and how much they dislike hanging it every year. Permanent lighting solves that, and we want every install to look clean, work reliably, and be easy to use.</p></div>
  <div><img class="photo" src="../assets/permanent-lighting.jpg" alt="Home with permanent roofline lighting" loading="lazy"></div>
</section>
<section class="gray pad"><div class="wrap two">
  <div><img class="photo" src="../assets/lakeside-lighting.jpg" alt="Lakeside home with permanent lighting" loading="lazy"></div>
  <div><h2>Our Values</h2>
  <p>Our work is guided by a few simple values. We believe honesty builds trust, hard work earns respect, and taking ownership leads to better results. These values shape how we quote, install, and support every customer.</p>
  <ul><li>Integrity in communication and transparent pricing</li><li>Personal responsibility for every job we take on</li><li>Strong work ethic with no shortcuts</li><li>Respect for every home, property, and customer</li></ul></div>
</div></section>
{trimlight(rel, "about")}
{cta(rel, "Let&rsquo;s Light Up Your Home", "Request a free quote and we&rsquo;ll plan the layout for your roofline.")}
""" + bottom(rel)
    write("about-us/index.html", html)


# ----------------------------------------------------------------------------
# CONTACT
# ----------------------------------------------------------------------------
def contact():
    rel = "../"
    title = f"Contact Us | {NAME} — Lancaster, PA"
    desc = "Request a free permanent lighting quote from Hooks Permanent Lighting in Lancaster, PA."
    html = head(title, desc, "contact-us/", rel) + top(rel, "contact-us/") + f"""
{page_title("Contact Us")}
<section class="wrap two pad" style="align-items:start">
  <div><h2>Get a Free Quote</h2><p>Tell us about your home and we&rsquo;ll get back to you with a quote.</p>{jobber_embed()}</div>
  <div><h2>Reliable Permanent Lighting, Installed Right.</h2>
  <p>Ready to get started? Send us a quote request and we&rsquo;ll plan the layout for your roofline.</p>
  <img class="photo" src="../assets/permanent-lighting.jpg" alt="Home with permanent roofline lighting" loading="lazy">
  <h4>Service Area:</h4><p>{SERVICE_AREA}</p>
  {"<h4>Contact:</h4>" + contact_block(rel) if (PHONE_TEL or EMAIL) else ""}</div>
</section>
{xpromo(rel)}
""" + bottom(rel)
    write("contact-us/index.html", html)


def extras():
    write("404.html", f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | {NAME}</title><body style="font-family:system-ui;text-align:center;padding:90px 20px;color:#001838"><h1>Page not found</h1><p><a href="/">Back to the {NAME} home page</a>.</p></body>""")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    urls = ["", "permanent-lighting/", "about-us/", "contact-us/"]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"<url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")


if __name__ == "__main__":
    home(); pl_page(); about(); contact(); extras()
    print("built")
