"""Builds the SVG images used in the profile README, in a light and a dark version.

Run:  python3 tools/build_assets.py
Edit the content dictionaries below, then re-run. GitHub picks the light or dark
file through the <picture> tags in README.md.
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

THEMES = {
    "light": dict(bg="#ffffff", surface="#f6f8fa", surface2="#eaeef2", ink="#1f2328", ink2="#424a53",
                  muted="#656d76", rule="#d0d7de", accent="#6a3fb5", c1="#0d7563", c2="#6a3fb5",
                  c3="#b04a17", c4="#8c959f", soft1="#daefe9", soft2="#ebe3fa", soft3="#fae4d6"),
    "dark": dict(bg="#0d1117", surface="#161b22", surface2="#21262d", ink="#e6edf3", ink2="#c9d1d9",
                 muted="#8b949e", rule="#30363d", accent="#bb9ff2", c1="#4fc9ad", c2="#bb9ff2",
                 c3="#f0925a", c4="#6e7681", soft1="#0e2a25", soft2="#231b37", soft3="#2f1810"),
}


def svg(w, h, body, t, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
            f'<style>text{{font-family:{FONT}}} .m{{font-family:{MONO}}}</style>{body}</svg>')


def segbar(x, y, w, t, h=6):
    parts = [(2.2, t["c1"]), (1.1, t["rule"]), (1.5, t["c2"]), (.7, t["rule"]), (1.1, t["c3"]), (3.4, t["rule"])]
    tot = sum(p for p, _ in parts); gap = 4; avail = w - gap * (len(parts) - 1); cx = x; out = ""
    for p, c in parts:
        pw = avail * p / tot
        out += f'<rect x="{cx:.1f}" y="{y}" width="{pw:.1f}" height="{h}" rx="1.5" fill="{c}"/>'
        cx += pw + gap
    return out


# ---------------------------------------------------------------- header
def header(t):
    W, H = 1200, 340
    b = f'<rect width="{W}" height="{H}" rx="14" fill="{t["surface"]}" stroke="{t["rule"]}"/>'
    b += segbar(48, 40, 520, t)
    b += f'<text x="48" y="92" font-size="14" font-weight="600" letter-spacing="2.4" fill="{t["muted"]}">PHD CANDIDATE  ·  COMPUTER VISION  ·  UNIVERSITY OF VICTORIA</text>'
    b += f'<text x="46" y="160" font-size="62" font-weight="700" letter-spacing="-1.5" fill="{t["ink"]}">Ali Soltaninezhad</text>'
    b += f'<text x="48" y="206" font-size="25" fill="{t["ink2"]}">Computer vision that works in the real world.</text>'
    chips = ["Action detection", "Video understanding", "Privacy", "Deployment"]
    cx = 48
    for c in chips:
        w = 22 + len(c) * 7.4
        b += f'<rect x="{cx}" y="244" width="{w:.0f}" height="30" rx="15" fill="{t["bg"]}" stroke="{t["rule"]}"/>'
        b += f'<text x="{cx + w / 2:.0f}" y="264" font-size="13.5" text-anchor="middle" fill="{t["ink2"]}">{c}</text>'
        cx += w + 8

    # right: a video timeline with action tubes and a moving playhead
    X0, X1 = 840, 1150
    tracks = [
        ("actor 1", [(0.00, 0.30, "c1"), (0.42, 0.78, "c1")]),
        ("actor 2", [(0.12, 0.50, "c2"), (0.62, 0.95, "c1")]),
        ("actor 3", [(0.30, 0.46, "c3"), (0.70, 0.86, "c2")]),
    ]
    b += f'<text x="{X0}" y="84" font-size="12" class="m" fill="{t["muted"]}">detections over time</text>'
    for i in range(9):  # frame ticks
        fx = X0 + (X1 - X0) * i / 8
        b += f'<rect x="{fx - 13:.0f}" y="98" width="26" height="18" rx="3" fill="{t["surface2"]}" stroke="{t["rule"]}"/>'
    for r, (lab, segs) in enumerate(tracks):
        y = 140 + r * 46
        b += f'<line x1="{X0}" y1="{y + 11}" x2="{X1}" y2="{y + 11}" stroke="{t["rule"]}" stroke-dasharray="2 5"/>'
        b += f'<text x="{X0 - 12}" y="{y + 15}" font-size="12" class="m" text-anchor="end" fill="{t["muted"]}">{lab}</text>'
        for s, e, c in segs:
            sx = X0 + (X1 - X0) * s; ex = X0 + (X1 - X0) * e
            b += f'<rect x="{sx:.0f}" y="{y}" width="{ex - sx:.0f}" height="22" rx="5" fill="{t[c]}" opacity=".9"/>'
    # a missed event: dashed outline nobody detected
    mx = X0 + (X1 - X0) * 0.08
    b += f'<rect x="{mx:.0f}" y="{140 + 2 * 46}" width="{(X1 - X0) * 0.16:.0f}" height="22" rx="5" fill="none" stroke="{t["c3"]}" stroke-width="1.6" stroke-dasharray="4 3"/>'
    b += f'<text x="{mx + (X1 - X0) * 0.08:.0f}" y="{140 + 2 * 46 + 40}" font-size="12" class="m" text-anchor="middle" fill="{t["c3"]}">missed?</text>'
    b += (f'<g><line x1="{X0}" y1="94" x2="{X0}" y2="290" stroke="{t["accent"]}" stroke-width="2"/>'
          f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{X1 - X0} 0" dur="7s" repeatCount="indefinite"/></g>')
    return svg(W, H, b, t, "Ali Soltaninezhad. Computer vision that works in the real world.")


# ---------------------------------------------------------------- research strip
RESEARCH = [
    ("01", "Spatio-temporal", "action detection", "Who does what, where and when, in long video.", "c1"),
    ("02", "Human review of", "detector errors", "Point a limited review budget at what the model missed.", "c2"),
    ("03", "Privacy-preserving", "video", "Mask people without breaking the task downstream.", "c3"),
    ("04", "Robust vision", "at sea", "Spray, glare, occlusion and a moving deck.", "c4"),
]


def research(t):
    W, H, n, gap = 1200, 190, 4, 16
    tw = (W - gap * (n - 1)) / n; b = ""
    for i, (idx, l1, l2, d, c) in enumerate(RESEARCH):
        x = i * (tw + gap)
        b += f'<rect x="{x:.0f}" y="1" width="{tw:.0f}" height="{H - 2}" rx="10" fill="{t["surface"]}" stroke="{t["rule"]}"/>'
        b += f'<rect x="{x + 20:.0f}" y="22" width="44" height="5" rx="2" fill="{t[c]}"/>'
        b += f'<text x="{x + tw - 20:.0f}" y="30" font-size="13" class="m" text-anchor="end" fill="{t["muted"]}">{idx}</text>'
        b += f'<text x="{x + 20:.0f}" y="68" font-size="21" font-weight="650" fill="{t["ink"]}">{l1}</text>'
        b += f'<text x="{x + 20:.0f}" y="94" font-size="21" font-weight="650" fill="{t["ink"]}">{l2}</text>'
        words, lines, cur = d.split(), [], ""
        for w_ in words:
            if len(cur) + len(w_) > 30:
                lines.append(cur.strip()); cur = ""
            cur += w_ + " "
        lines.append(cur.strip())
        for j, ln in enumerate(lines):
            b += f'<text x="{x + 20:.0f}" y="{128 + j * 21}" font-size="15" fill="{t["ink2"]}">{escape(ln)}</text>'
    return svg(W, H, b, t, "Research areas")


# ---------------------------------------------------------------- project cards
PROJECTS = {
    "vidquery": dict(kind="DEPLOYMENT", title="vidquery", c="c1",
                     lines=["Text-to-video person search with VLM verification.",
                            "PyTorch, ONNX Runtime and TensorRT behind one",
                            "interface, served with FastAPI, Docker and Slurm."],
                     tags=["TensorRT", "FastAPI", "FAISS", "vLLM"]),
    "paper-semantic-map": dict(kind="CLAUDE SKILL", title="paper-semantic-map", c="c2",
                               lines=["Turns papers into deep visual HTML maps and an",
                                      "archive that tracks gaps in a field against",
                                      "your own research question."],
                               tags=["Claude", "Research", "HTML"]),
    "trapcounter": dict(kind="DATASET  ·  CRV 2025 ORAL", title="TrapCounter / DTCFT", c="c3",
                        lines=["First public dataset for detecting, tracking and",
                               "counting fishing traps in real vessel footage.",
                               "16,500 annotated frames from BC waters."],
                        tags=["Tracking", "Optical flow", "Marine"]),
    "ihard46": dict(kind="DATASET", title="IHARD46", c="c4",
                    lines=["Imbalanced human action recognition dataset",
                           "with 46 action classes, built to study long-tail",
                           "action recognition."],
                    tags=["Action recognition", "Long tail"]),
}


def card(p, t):
    W, H = 580, 210
    b = f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="{t["surface"]}" stroke="{t["rule"]}"/>'
    b += f'<rect x="1" y="1" width="6" height="{H - 2}" rx="3" fill="{t[p["c"]]}"/>'
    b += f'<text x="30" y="38" font-size="12" font-weight="600" letter-spacing="1.8" fill="{t["muted"]}">{escape(p["kind"])}</text>'
    b += f'<text x="{W - 28}" y="40" font-size="20" text-anchor="end" fill="{t["muted"]}">&#8599;</text>'
    b += f'<text x="30" y="74" font-size="24" font-weight="700" fill="{t["ink"]}">{escape(p["title"])}</text>'
    for i, ln in enumerate(p["lines"]):
        b += f'<text x="30" y="{106 + i * 22}" font-size="15.5" fill="{t["ink2"]}">{escape(ln)}</text>'
    cx = 30
    for tag in p["tags"]:
        w = 18 + len(tag) * 7.3
        b += f'<rect x="{cx}" y="166" width="{w:.0f}" height="26" rx="13" fill="{t["bg"]}" stroke="{t["rule"]}"/>'
        b += f'<text x="{cx + w / 2:.0f}" y="183.5" font-size="13" class="m" text-anchor="middle" fill="{t["ink2"]}">{escape(tag)}</text>'
        cx += w + 8
    return svg(W, H, b, t, p["title"])


# ---------------------------------------------------------------- publication timeline
PUBS = [  # year, label, first author, oral
    (2021, "ICWR", False, False), (2021, "ICCKE", True, False), (2022, "KBS", False, False),
    (2025, "CRV", True, True), (2026, "ICPR", True, True), (2026, "ICPR", False, False),
    (2026, "ECCVW", True, True), (2027, "WACV", True, False),
]


def timeline(t):
    W, H = 1200, 200
    years = list(range(2021, 2028)); X0, X1, Y = 60, 1140, 150
    b = f'<line x1="{X0 - 20}" y1="{Y}" x2="{X1 + 20}" y2="{Y}" stroke="{t["rule"]}" stroke-width="2"/>'
    for i, yv in enumerate(years):
        x = X0 + (X1 - X0) * i / (len(years) - 1)
        b += f'<line x1="{x:.0f}" y1="{Y - 5}" x2="{x:.0f}" y2="{Y + 5}" stroke="{t["rule"]}" stroke-width="2"/>'
        b += f'<text x="{x:.0f}" y="{Y + 32}" font-size="15" class="m" text-anchor="middle" fill="{t["muted"]}">{yv}</text>'
    byyear = {}
    for yv, lab, first, oral in PUBS:
        byyear.setdefault(yv, []).append((lab, first, oral))
    for yv, items in byyear.items():
        items.sort(key=lambda it: not it[1])  # first-author pills sit nearest the axis
        x = X0 + (X1 - X0) * (yv - years[0]) / (len(years) - 1)
        for k, (lab, first, oral) in enumerate(items):
            y = Y - 34 - k * 38
            col = t["c2"] if first else t["c4"]
            w = 26 + len(lab) * 9 + (34 if oral else 0)
            b += f'<rect x="{x - w / 2:.0f}" y="{y - 15}" width="{w:.0f}" height="28" rx="14" fill="{t["soft2"] if first else t["surface2"]}" stroke="{col}"/>'
            tx = x - (17 if oral else 0)
            b += f'<text x="{tx:.0f}" y="{y + 4}" font-size="14" font-weight="650" text-anchor="middle" fill="{t["ink"] if first else t["ink2"]}">{lab}</text>'
            if oral:
                b += f'<text x="{x + w / 2 - 22:.0f}" y="{y + 3.5}" font-size="10.5" font-weight="700" letter-spacing=".8" text-anchor="middle" fill="{t["c3"]}">ORAL</text>'
        b += f'<circle cx="{x:.0f}" cy="{Y}" r="6" fill="{t["accent"]}"/>'
    # legend
    b += f'<rect x="40" y="6" width="14" height="14" rx="7" fill="{t["soft2"]}" stroke="{t["c2"]}"/>'
    b += f'<text x="60" y="18" font-size="13" fill="{t["ink2"]}">first author</text>'
    b += f'<rect x="160" y="6" width="14" height="14" rx="7" fill="{t["surface2"]}" stroke="{t["c4"]}"/>'
    b += f'<text x="180" y="18" font-size="13" fill="{t["ink2"]}">co-author</text>'
    return svg(W, H, b, t, "Publication timeline, 2021 to 2027")


def footer(t):
    W, H = 1200, 24
    return svg(W, H, segbar(0, 9, W, t), t, "")


for name, t in THEMES.items():
    (OUT / f"header-{name}.svg").write_text(header(t))
    (OUT / f"research-{name}.svg").write_text(research(t))
    (OUT / f"timeline-{name}.svg").write_text(timeline(t))
    (OUT / f"footer-{name}.svg").write_text(footer(t))
    for key, p in PROJECTS.items():
        (OUT / f"card-{key}-{name}.svg").write_text(card(p, t))
print("wrote", len(list(OUT.glob("*.svg"))), "files to", OUT)
