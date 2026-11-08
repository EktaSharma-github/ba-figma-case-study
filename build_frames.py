"""Generates Figma-importable SVG frames for the Halden Logistics
expense-reimbursement case study. Drag any output SVG into Figma and it
becomes editable vector layers (text stays text)."""
from pathlib import Path
from html import escape

OUT = Path(__file__).parent / "figma-frames"
OUT.mkdir(exist_ok=True)

# Design tokens (mirror these as Figma variables)
INK = "#1B2430"; MUTED = "#5B6676"; LINE = "#C9D1DB"; PAPER = "#FFFFFF"
CANVAS = "#F3F5F8"; BLUE = "#1F5FAD"; BLUE_T = "#E3EDF9"; TEAL = "#0F7B6C"
TEAL_T = "#DDF2EE"; RED = "#B93A32"; RED_T = "#FBE6E4"; AMBER = "#A86A00"
AMBER_T = "#FDF0D5"; VIOLET = "#5B4BB7"; VIOLET_T = "#ECE9FA"
FONT = "IBM Plex Sans, Helvetica, Arial, sans-serif"
MONO = "IBM Plex Mono, Menlo, monospace"


class Svg:
    def __init__(self, w, h, title):
        self.w, self.h, self.items = w, h, []
        self.title = title

    def add(self, s):
        self.items.append(s)

    def rect(self, x, y, w, h, fill=PAPER, stroke=None, rx=0, sw=1, dash=None, name=None):
        a = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        if dash: a += f' stroke-dasharray="{dash}"'
        n = f' id="{name}"' if name else ""
        self.add(f'<rect{n} x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{a}/>')

    def text(self, x, y, s, size=14, fill=INK, weight=400, anchor="start", font=FONT, ls=None):
        l = f' letter-spacing="{ls}"' if ls else ""
        self.add(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
                 f'fill="{fill}" text-anchor="{anchor}"{l}>{escape(s)}</text>')

    def lines(self, x, y, rows, size=13, fill=INK, weight=400, anchor="start", lh=None):
        lh = lh or size * 1.35
        for i, r in enumerate(rows):
            self.text(x, y + i * lh, r, size, fill, weight, anchor)

    def line(self, x1, y1, x2, y2, stroke=LINE, sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def path(self, d, stroke=INK, sw=1.5, fill="none", arrow=True, dash=None):
        m = ' marker-end="url(#arr)"' if arrow else ""
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{m}{ds}/>')

    def circle(self, cx, cy, r, fill, stroke=None, sw=1.5):
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{s}/>')

    def group(self, name):
        self.add(f'<g id="{escape(name)}">')

    def end(self):
        self.add("</g>")

    def header(self, eyebrow, title, sub):
        self.rect(0, 0, self.w, self.h, CANVAS, name="Frame background")
        self.text(48, 58, eyebrow.upper(), 12, BLUE, 600, ls="1.2")
        self.text(48, 92, title, 30, INK, 700)
        self.text(48, 120, sub, 15, MUTED)
        self.text(self.w - 48, 58, "Halden Logistics · Expense Reimbursement Redesign", 12, MUTED, anchor="end")

    def save(self, fname):
        defs = ('<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
                f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>')
        body = "\n".join(self.items)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
               f'viewBox="0 0 {self.w} {self.h}"><title>{escape(self.title)}</title>{defs}\n{body}\n</svg>')
        (OUT / fname).write_text(svg)


def pill(s, x, y, label, fill, color, size=11):
    w = len(label) * size * 0.62 + 18
    s.rect(x, y, w, 22, fill, rx=11)
    s.text(x + w / 2, y + 15, label, size, color, 600, "middle")
    return w


# ---------------------------------------------------------------- 01 Stakeholder map
def stakeholders():
    s = Svg(1440, 900, "01 Stakeholder Map")
    s.header("01 · Discovery", "Stakeholder map", "Power / interest grid built from 11 interviews and 2 process walkthroughs")
    gx, gy, gw, gh = 120, 170, 820, 640
    quads = [("Keep satisfied", gx, gy, AMBER_T), ("Manage closely", gx + gw / 2, gy, BLUE_T),
             ("Monitor", gx, gy + gh / 2, CANVAS), ("Keep informed", gx + gw / 2, gy + gh / 2, TEAL_T)]
    for name, x, y, f in quads:
        s.rect(x, y, gw / 2, gh / 2, f, LINE)
        s.text(x + 16, y + 28, name.upper(), 11, MUTED, 600, ls="1")
    s.path(f"M{gx} {gy+gh} L{gx} {gy-10}", INK, 1.5)
    s.path(f"M{gx} {gy+gh} L{gx+gw+10} {gy+gh}", INK, 1.5)
    s.add(f'<text x="{gx-24}" y="{gy+gh/2}" font-family="{FONT}" font-size="13" font-weight="600" fill="{INK}" text-anchor="middle" transform="rotate(-90 {gx-24} {gy+gh/2})">Power</text>')
    s.text(gx + gw / 2, gy + gh + 36, "Interest in the change", 13, INK, 600, "middle")
    people = [  # name, role, x, y (0..1), colour
        ("CFO", "Sponsor", .80, .12, BLUE), ("AP Lead", "Process owner", .78, .28, BLUE),
        ("IT / ERP team", "System owner", .62, .36, BLUE), ("Internal Audit", "Compliance", .22, .18, AMBER),
        ("Tax team", "GST recovery", .30, .38, AMBER), ("Line managers", "Approvers", .72, .64, TEAL),
        ("Field staff", "120 claimants/mo", .76, .80, TEAL), ("Travel desk", "Bookings", .26, .80, MUTED),
    ]
    for n, r, px, py, c in people:
        x, y = gx + px * gw, gy + py * gh
        s.group(f"Stakeholder / {n}")
        s.circle(x, y, 9, c)
        s.text(x + 16, y - 2, n, 14, INK, 600)
        s.text(x + 16, y + 15, r, 12, MUTED)
        s.end()
    # notes panel
    px = 1000
    s.rect(px, 170, 392, 640, PAPER, LINE, 8)
    s.text(px + 24, 206, "What we heard", 18, INK, 700)
    quotes = [
        ("AP Lead", ["“We key every receipt twice: once in", "the spreadsheet, once in the ERP.”"]),
        ("Field staff", ["“I wait three weeks to get my own", "money back.”"]),
        ("Line manager", ["“Approvals arrive as email attachments.", "I can't see the policy limits.”"]),
        ("Internal Audit", ["“18% of claims last year were missing", "an itemised receipt.”"]),
    ]
    y = 250
    for who, q in quotes:
        s.rect(px + 24, y - 14, 3, 58, BLUE)
        s.lines(px + 40, y, q, 13, INK)
        s.text(px + 40, y + 42, who, 12, MUTED, 600)
        y += 100
    s.line(px + 24, y - 10, px + 368, y - 10)
    s.text(px + 24, y + 20, "RACI owner for sign-off: CFO", 13, INK, 600)
    s.text(px + 24, y + 42, "Process owner: AP Lead", 13, MUTED)
    s.save("01-stakeholder-map.svg")


# ---------------------------------------------------------------- swimlane helpers
LANE_X, LANE_LABEL_W = 48, 150


def lanes(s, names, top, lane_h, width):
    for i, n in enumerate(names):
        y = top + i * lane_h
        s.rect(LANE_X, y, width, lane_h, PAPER if i % 2 == 0 else "#FAFBFC", LINE)
        s.rect(LANE_X, y, LANE_LABEL_W, lane_h, "#EEF1F5", LINE)
        s.text(LANE_X + LANE_LABEL_W / 2, y + lane_h / 2 + 5, n, 14, INK, 600, "middle")


def task(s, cx, cy, label_rows, fill=PAPER, stroke=INK, w=150, h=58):
    s.rect(cx - w / 2, cy - h / 2, w, h, fill, stroke, 8, 1.4)
    n = len(label_rows)
    s.lines(cx, cy - (n - 1) * 8 + 4, label_rows, 12.5, INK, 500, "middle", 16)


def gateway(s, cx, cy, label, r=26, below=False):
    s.add(f'<polygon points="{cx},{cy-r} {cx+r},{cy} {cx},{cy+r} {cx-r},{cy}" fill="{AMBER_T}" stroke="{INK}" stroke-width="1.4"/>')
    s.text(cx, cy + 4, "?", 14, INK, 700, "middle")
    s.text(cx, cy + r + 18 if below else cy - r - 8, label, 11.5, MUTED, 500, "middle")


def event(s, cx, cy, end=False, label=None):
    s.circle(cx, cy, 16, PAPER, INK, 3.5 if end else 1.6)
    if label: s.text(cx, cy + 34, label, 11.5, MUTED, 500, "middle")


def pain(s, x, y, n):
    s.circle(x, y, 12, RED)
    s.text(x, y + 4.5, str(n), 12, PAPER, 700, "middle")


# ---------------------------------------------------------------- 02 As-Is
def as_is():
    s = Svg(1920, 1000, "02 As-Is Process")
    s.header("02 · Current state", "As-Is: expense reimbursement (BPMN swimlane)",
             "Average cycle time 14.2 working days · 31% of claims returned at least once")
    top, lh, width = 160, 150, 1824
    lanes(s, ["Employee", "Line manager", "Finance / AP", "ERP"], top, lh, width)
    c = lambda i: top + i * lh + lh / 2
    x0 = 260
    event(s, x0, c(0), label="Trip ends")
    task(s, 400, c(0), ["Fill Excel template"])
    task(s, 580, c(0), ["Scan paper receipts"])
    task(s, 760, c(0), ["Email to manager"])
    task(s, 760, c(1), ["Open attachment,", "check vs policy PDF"])
    gateway(s, 940, c(1), "Within policy?", below=True)
    task(s, 1100, c(1), ["Forward email", "to AP inbox"])
    task(s, 1100, c(2), ["Re-key lines", "into ERP"])
    task(s, 1290, c(2), ["Match receipts", "manually"])
    gateway(s, 1460, c(2), "Receipts OK?")
    task(s, 1620, c(3), ["Post invoice,", "weekly pay run"])
    event(s, 1800, c(3), True, "Paid")
    # flows
    s.path(f"M{x0+16} {c(0)} L325 {c(0)}"); s.path(f"M475 {c(0)} L505 {c(0)}")
    s.path(f"M655 {c(0)} L685 {c(0)}"); s.path(f"M760 {c(0)+29} L760 {c(1)-29}")
    s.path(f"M835 {c(1)} L914 {c(1)}"); s.path(f"M966 {c(1)} L1025 {c(1)}")
    s.text(990, c(1) - 8, "Yes", 11, MUTED)
    s.path(f"M940 {c(1)-26} L940 {c(0)-40} L400 {c(0)-40} L400 {c(0)-29}", RED, 1.4, dash="5 4")
    s.text(950, c(0) - 46, "No: return by email", 11, RED, 600)
    s.path(f"M1100 {c(1)+29} L1100 {c(2)-29}"); s.path(f"M1175 {c(2)} L1215 {c(2)}")
    s.path(f"M1365 {c(2)} L1434 {c(2)}")
    s.path(f"M1486 {c(2)} L1620 {c(2)} L1620 {c(3)-29}"); s.text(1500, c(2) - 8, "Yes", 11, MUTED)
    s.path(f"M1460 {c(2)+26} L1460 {c(2)+58} L580 {c(2)+58} L580 {c(0)+29}", RED, 1.4, dash="5 4")
    s.text(1000, c(2) + 52, "No: chase employee for missing receipt", 11, RED, 600)
    s.path(f"M1695 {c(3)} L1784 {c(3)}")
    # pain points
    for n, (x, y) in enumerate([(470, c(0) - 30), (830, c(1) - 30), (1170, c(2) - 30),
                                (1360, c(2) - 30), (1690, c(3) - 30)], 1):
        pain(s, x, y, n)
    # legend / pain list
    ly = top + 4 * lh + 40
    s.text(48, ly, "Pain points", 16, INK, 700)
    pains = ["Manual template, no validation (17% arithmetic errors)",
             "Policy limits live in a PDF; approvers guess",
             "Double data entry: 6.5 min per claim line",
             "Receipt matching by eye; no OCR",
             "Weekly pay run adds up to 5 days"]
    for i, p in enumerate(pains):
        x = 48 + (i % 3) * 600; y = ly + 34 + (i // 3) * 34
        pain(s, x + 12, y - 4, i + 1); s.text(x + 34, y, p, 13, INK)
    s.save("02-as-is-process.svg")


# ---------------------------------------------------------------- 03 To-Be
def to_be():
    s = Svg(1920, 1000, "03 To-Be Process")
    s.header("03 · Future state", "To-Be: digital claim with policy engine and ERP integration",
             "Target cycle time 3 working days · auto-approval for in-policy claims under ₹5,000")
    top, lh, width = 160, 150, 1824
    lanes(s, ["Employee", "Expense app", "Line manager", "Finance / AP", "ERP"], top, lh - 20, width)
    lh -= 20
    c = lambda i: top + i * lh + lh / 2
    event(s, 260, c(0), label="Expense incurred")
    task(s, 410, c(0), ["Snap receipt", "in mobile app"], BLUE_T, BLUE)
    task(s, 410, c(1), ["OCR extracts", "merchant, date, tax"], TEAL_T, TEAL)
    task(s, 600, c(1), ["Policy engine", "validates lines"], TEAL_T, TEAL)
    gateway(s, 780, c(1), "Risk band?")
    task(s, 960, c(1), ["Auto-approve", "(low risk)"], TEAL_T, TEAL)
    task(s, 960, c(2), ["Approve in app", "with policy context"], BLUE_T, BLUE)
    task(s, 1160, c(3), ["Exception queue", "only flagged lines"], BLUE_T, BLUE)
    task(s, 1360, c(4), ["Post via API,", "GL auto-coded"], VIOLET_T, VIOLET)
    task(s, 1560, c(4), ["Daily payment", "batch"], VIOLET_T, VIOLET)
    event(s, 1760, c(4), True, "Paid + notified")
    s.path(f"M276 {c(0)} L335 {c(0)}"); s.path(f"M410 {c(0)+29} L410 {c(1)-29}")
    s.path(f"M485 {c(1)} L525 {c(1)}"); s.path(f"M675 {c(1)} L754 {c(1)}")
    s.path(f"M806 {c(1)} L885 {c(1)}"); s.text(820, c(1) - 8, "Low", 11, MUTED)
    s.path(f"M780 {c(1)+26} L780 {c(2)} L885 {c(2)}"); s.text(790, c(2) - 8, "Medium", 11, MUTED)
    s.path(f"M780 {c(1)+26} L780 {c(3)} L1085 {c(3)}"); s.text(790, c(3) - 8, "High / exception", 11, MUTED)
    s.path(f"M1035 {c(1)} L1360 {c(1)} L1360 {c(4)-29}")
    s.path(f"M1035 {c(2)} L1300 {c(2)} L1300 {c(4)-29}")
    s.path(f"M1235 {c(3)} L1260 {c(3)} L1260 {c(4)} L1285 {c(4)}")
    s.path(f"M1435 {c(4)} L1485 {c(4)}"); s.path(f"M1635 {c(4)} L1744 {c(4)}")
    # legend
    ly = top + 5 * lh + 44
    s.text(48, ly, "Legend", 16, INK, 700)
    for i, (lbl, f, st) in enumerate([("Human task", BLUE_T, BLUE), ("Automated (app)", TEAL_T, TEAL),
                                      ("System integration", VIOLET_T, VIOLET)]):
        x = 48 + i * 260; s.rect(x, ly + 18, 28, 20, f, st, 4); s.text(x + 38, ly + 33, lbl, 13, INK)
    s.text(900, ly, "Improvements traced to pain points", 16, INK, 700)
    imp = ["1 → OCR + validation at capture", "2 → Policy shown inline to approver",
           "3 → Single entry, API posting", "4 → OCR + tax extraction", "5 → Daily payment batch"]
    for i, t in enumerate(imp):
        s.text(900 + (i % 3) * 320, ly + 33 + (i // 3) * 26, t, 13, TEAL, 600)
    s.save("03-to-be-process.svg")


# ---------------------------------------------------------------- 04 Journey map
def journey():
    s = Svg(1920, 1080, "04 User Journey Map")
    s.header("04 · Persona journey", "Journey map: Priya, regional sales executive",
             "Travels 9 days a month · submits ~22 receipts · smartphone-first")
    stages = ["Spend", "Collect receipts", "Prepare claim", "Approval", "Payment"]
    x0, colw, top = 220, 330, 170
    rows = [("Doing", 120), ("Thinking", 100), ("Feeling", 200), ("Pain points", 110), ("Opportunities", 120)]
    s.rect(48, top, 1824, 52, INK, rx=6)
    for i, st in enumerate(stages):
        s.text(x0 + i * colw + colw / 2, top + 32, f"{i+1}. {st}", 15, PAPER, 600, "middle")
    y = top + 64
    content = {
        "Doing": [["Pays hotel and taxi", "on personal card"], ["Stuffs receipts", "into wallet"],
                  ["Types 22 rows into", "Excel on a Sunday"], ["Waits; chases", "manager on chat"],
                  ["Checks bank", "account daily"]],
        "Thinking": [["“Will this be", "within policy?”"], ["“Did I lose the", "taxi receipt?”"],
                     ["“What's the GL", "code for tolls?”"], ["“Has anyone", "even opened it?”"],
                     ["“Why is it short", "by ₹640?”"]],
        "Pain points": [["Policy unclear", "at point of spend"], ["Thermal receipts", "fade"],
                        ["45 min per claim"], ["No status", "visibility"], ["Deductions", "unexplained"]],
        "Opportunities": [["Show limit before", "booking"], ["Capture photo", "at once"],
                          ["Auto-fill from OCR"], ["Push status", "updates"], ["Line-level payout", "breakdown"]],
    }
    feel = [0.45, 0.25, 0.10, 0.20, 0.55]  # 0 = frustrated, 1 = happy
    for name, h in rows:
        s.rect(48, y, 1824, h, PAPER, LINE, 6)
        s.text(64, y + 28, name.upper(), 11, MUTED, 600, ls="1")
        for i in range(1, 5):
            s.line(x0 + i * colw, y + 12, x0 + i * colw, y + h - 12, LINE, 1, "3 4")
        if name == "Feeling":
            pts = []
            for i, f in enumerate(feel):
                px = x0 + i * colw + colw / 2; py = y + h - 30 - f * (h - 60)
                pts.append((px, py))
            s.line(x0, y + h / 2, x0 + 5 * colw, y + h / 2, LINE, 1, "2 4")
            d = "M" + " L".join(f"{px:.0f} {py:.0f}" for px, py in pts)
            s.path(d, BLUE, 2.5, arrow=False)
            for (px, py), f in zip(pts, feel):
                col = RED if f < .3 else (AMBER if f < .5 else TEAL)
                s.circle(px, py, 8, col, PAPER, 2)
            s.text(x0 - 12, y + 34, "Happy", 11, MUTED, anchor="end")
            s.text(x0 - 12, y + h - 22, "Frustrated", 11, MUTED, anchor="end")
        else:
            col = RED if name == "Pain points" else (TEAL if name == "Opportunities" else INK)
            wt = 600 if name in ("Pain points", "Opportunities") else 400
            for i, r in enumerate(content[name]):
                s.lines(x0 + i * colw + 24, y + 38, r, 13.5, col, wt, lh=19)
        y += h + 12
    s.save("04-journey-map.svg")


# ---------------------------------------------------------------- 05 Wireframes
def phone(s, x, y, title, step):
    w, h = 300, 620
    s.group(f"Mobile / {title}")
    s.rect(x, y, w, h, PAPER, INK, 28, 2)
    s.rect(x + 110, y + 12, 80, 8, LINE, rx=4)
    s.text(x + 20, y + 58, step, 11, MUTED, 600, ls="1")
    s.text(x + 20, y + 82, title, 18, INK, 700)
    return x + 20, y + 100, w - 40


def field(s, x, y, w, label, value, state=None):
    s.text(x, y, label, 11, MUTED, 600)
    stroke = RED if state == "err" else (TEAL if state == "ok" else LINE)
    s.rect(x, y + 6, w, 36, PAPER, stroke, 6, 1.4)
    s.text(x + 12, y + 29, value, 13, INK)
    if state == "ok": s.text(x + w - 12, y + 29, "OCR ✓", 11, TEAL, 600, "end")
    return y + 58


def button(s, x, y, w, label, primary=True):
    s.rect(x, y, w, 42, BLUE if primary else PAPER, None if primary else BLUE, 8, 1.4)
    s.text(x + w / 2, y + 26, label, 14, PAPER if primary else BLUE, 600, "middle")


def wireframes():
    s = Svg(1920, 1000, "05 Wireframes")
    s.header("05 · Solution design", "Low-fi wireframes: capture → review → approve",
             "Mid-fidelity, grayscale + one accent. Annotations map each screen to requirement IDs.")
    # Screen 1: capture
    x, y, w = phone(s, 48, 170, "Scan receipt", "STEP 1 OF 3")
    s.rect(x, y, w, 300, "#E9EDF2", LINE, 10, 1, "6 5")
    s.rect(x + 50, y + 40, w - 100, 210, PAPER, MUTED, 4)
    for i in range(7): s.line(x + 66, y + 70 + i * 24, x + w - 66 - (i % 3) * 30, y + 70 + i * 24, LINE, 4)
    s.text(x + w / 2, y + 282, "Align receipt inside the frame", 12, MUTED, anchor="middle")
    s.circle(x + w / 2, y + 360, 30, PAPER, BLUE, 4); s.circle(x + w / 2, y + 360, 20, BLUE)
    s.text(x + w / 2, y + 420, "Upload from gallery", 13, BLUE, 600, "middle")
    s.end()
    # Screen 2: review
    x, y, w = phone(s, 388, 170, "Review expense", "STEP 2 OF 3")
    y2 = field(s, x, y + 10, w, "MERCHANT", "Hotel Saffron, Pune", "ok")
    y2 = field(s, x, y2, w, "DATE", "04 Nov 2026", "ok")
    y2 = field(s, x, y2, w, "CATEGORY", "Lodging ▾")
    y2 = field(s, x, y2, w, "AMOUNT (INR)", "6,850.00", "err")
    s.rect(x, y2 - 10, w, 54, RED_T, rx=6)
    s.lines(x + 12, y2 + 10, ["Over Pune lodging limit (₹5,500).", "Add a justification to continue."], 11.5, RED, 500, lh=16)
    button(s, x, y2 + 60, w, "Continue")
    s.end()
    # Screen 3: submitted
    x, y, w = phone(s, 728, 170, "Claim submitted", "STEP 3 OF 3")
    s.circle(x + w / 2, y + 60, 34, TEAL_T); s.text(x + w / 2, y + 70, "✓", 30, TEAL, 700, "middle")
    s.text(x + w / 2, y + 130, "EXP-2026-0412 · ₹14,230", 14, INK, 600, "middle")
    steps = [("Submitted", "04 Nov, 18:02", TEAL), ("Manager review", "Expected by 06 Nov", AMBER),
             ("Finance check", "Only if flagged", LINE), ("Paid", "Next daily batch", LINE)]
    for i, (a, b, col) in enumerate(steps):
        yy = y + 180 + i * 62
        s.circle(x + 14, yy, 9, col)
        if i < 3: s.line(x + 14, yy + 10, x + 14, yy + 52, LINE, 2)
        s.text(x + 36, yy + 4, a, 14, INK, 600); s.text(x + 36, yy + 22, b, 12, MUTED)
    button(s, x, y + 440, w, "Back to my claims", False)
    s.end()
    # Desktop approver
    dx, dy, dw, dh = 1080, 170, 792, 620
    s.group("Desktop / Approver queue")
    s.rect(dx, dy, dw, dh, PAPER, INK, 10, 2)
    s.rect(dx, dy, dw, 40, "#EEF1F5", rx=10); s.rect(dx, dy + 30, dw, 10, "#EEF1F5")
    for i, col in enumerate([RED, AMBER, TEAL]): s.circle(dx + 20 + i * 18, dy + 20, 5, col)
    s.text(dx + 24, dy + 80, "Approvals", 20, INK, 700)
    s.text(dx + 24, dy + 102, "7 waiting · 2 need attention", 13, MUTED)
    pill(s, dx + dw - 170, dy + 64, "Approve 5 in policy", BLUE, PAPER)
    cols = [("Employee", 24), ("Claim", 200), ("Amount", 330), ("Policy check", 450), ("Age", 640)]
    ty = dy + 140
    s.rect(dx + 12, ty - 22, dw - 24, 34, CANVAS, rx=4)
    for c_, off in cols: s.text(dx + off, ty, c_.upper(), 11, MUTED, 600, ls="0.8")
    data = [("Priya Nair", "EXP-0412", "₹14,230", ("1 line over limit", RED_T, RED), "1 d"),
            ("Arjun Mehta", "EXP-0409", "₹3,120", ("In policy", TEAL_T, TEAL), "1 d"),
            ("Sara Khan", "EXP-0405", "₹8,940", ("Missing receipt", AMBER_T, AMBER), "2 d"),
            ("Dev Patel", "EXP-0401", "₹2,450", ("In policy", TEAL_T, TEAL), "3 d"),
            ("Meera Iyer", "EXP-0398", "₹4,780", ("In policy", TEAL_T, TEAL), "3 d")]
    for i, (n, cl, amt, (st, f, col), age) in enumerate(data):
        ry = ty + 48 + i * 52
        if i == 0: s.rect(dx + 12, ry - 30, dw - 24, 48, BLUE_T, rx=4)
        s.text(dx + 24, ry, n, 14, INK, 600); s.text(dx + 200, ry, cl, 13, MUTED, font=MONO)
        s.text(dx + 400, ry, amt, 14, INK, 500, "end")
        pill(s, dx + 450, ry - 16, st, f, col); s.text(dx + 640, ry, age, 13, MUTED)
        s.line(dx + 12, ry + 20, dx + dw - 12, ry + 20, "#E6EAF0")
    s.rect(dx + 24, dy + 500, dw - 48, 96, CANVAS, rx=8)
    s.text(dx + 44, dy + 530, "Selected: Hotel Saffron, Pune · ₹6,850 vs limit ₹5,500", 13, INK, 600)
    s.text(dx + 44, dy + 552, "Justification: “Client site hotel; only option with availability.”", 13, MUTED)
    pill(s, dx + 44, dy + 564, "Approve", BLUE, PAPER); pill(s, dx + 140, dy + 564, "Return with note", PAPER, BLUE)
    s.end()
    # annotations
    notes = [(198, "FR-01, FR-02"), (538, "FR-03, FR-04, BR-07"), (878, "FR-09"), (1476, "FR-05, FR-06, NFR-03")]
    for xx, t in notes:
        s.rect(xx - 80, 820, 160, 30, AMBER_T, AMBER, 6, 1, "4 3")
        s.text(xx, 840, t, 12, AMBER, 600, "middle")
        s.line(xx, 795, xx, 820, AMBER, 1, "3 3")
    s.text(48, 900, "Annotation colour = requirement link. Every component on these screens is built from the shared library page (buttons, fields, pills, status steps).", 13, MUTED)
    s.save("05-wireframes.svg")


# ---------------------------------------------------------------- 06 Requirements & RTM
def requirements():
    s = Svg(1920, 1080, "06 Requirements & RTM")
    s.header("06 · Specification", "User stories, acceptance criteria and traceability",
             "MoSCoW-prioritised backlog · each requirement traced to a pain point, a screen and a UAT case")
    # story card
    s.rect(48, 160, 560, 420, PAPER, LINE, 10)
    s.text(72, 196, "FR-04 · Policy check at capture", 18, INK, 700)
    pill(s, 72, 210, "MUST", RED_T, RED); pill(s, 140, 210, "Sprint 2", BLUE_T, BLUE); pill(s, 232, 210, "5 pts", CANVAS, MUTED)
    s.lines(72, 268, ["As a claimant, I want to see when a line breaks", "policy before I submit, so that my claim is not", "returned days later."], 14, INK, lh=21)
    s.text(72, 352, "ACCEPTANCE CRITERIA (Gherkin)", 11, MUTED, 600, ls="1")
    gher = [("Given", "a lodging line in city tier B"), ("And", "the nightly rate exceeds ₹5,500"),
            ("When", "I tap Continue"), ("Then", "the amount field shows an error state"),
            ("And", "a justification field becomes mandatory"), ("And", "the line is tagged risk = Medium")]
    for i, (k, v) in enumerate(gher):
        yy = 382 + i * 30
        s.text(72, yy, k, 13, BLUE, 700, font=MONO); s.text(140, yy, v, 13, INK)
    # MoSCoW bar
    s.rect(48, 600, 560, 420, PAPER, LINE, 10)
    s.text(72, 636, "Backlog by priority (32 items)", 18, INK, 700)
    bars = [("Must", 14, RED), ("Should", 9, AMBER), ("Could", 6, BLUE), ("Won't (this release)", 3, MUTED)]
    for i, (l, n, col) in enumerate(bars):
        yy = 680 + i * 76
        s.text(72, yy, l, 13, INK, 600); s.text(584, yy, str(n), 13, INK, 600, "end")
        s.rect(72, yy + 12, 512, 18, CANVAS, rx=4); s.rect(72, yy + 12, 512 * n / 14, 18, col, rx=4)
    # RTM table
    tx, ty, tw = 648, 160, 1224
    s.rect(tx, ty, tw, 860, PAPER, LINE, 10)
    s.text(tx + 24, ty + 36, "Requirements traceability matrix", 18, INK, 700)
    hdr = [("ID", 24), ("Requirement", 110), ("Type", 520), ("Pain pt", 620), ("Screen", 720), ("UAT case", 880), ("Status", 1020)]
    hy = ty + 76
    s.rect(tx + 12, hy - 22, tw - 24, 34, CANVAS, rx=4)
    for h, o in hdr: s.text(tx + o, hy, h.upper(), 11, MUTED, 600, ls="0.8")
    rows = [
        ("FR-01", "Capture receipt via camera or upload", "Functional", "1", "Scan receipt", "UAT-101", ("Done", TEAL_T, TEAL)),
        ("FR-02", "OCR extracts merchant, date, amount, GST", "Functional", "1, 4", "Scan receipt", "UAT-102", ("Done", TEAL_T, TEAL)),
        ("FR-03", "Auto-suggest category and GL code", "Functional", "3", "Review", "UAT-103", ("In test", BLUE_T, BLUE)),
        ("FR-04", "Validate line against policy at capture", "Functional", "2", "Review", "UAT-104", ("In test", BLUE_T, BLUE)),
        ("FR-05", "Approver sees policy context per line", "Functional", "2", "Approvals", "UAT-105", ("Build", AMBER_T, AMBER)),
        ("FR-06", "Bulk-approve in-policy claims", "Functional", "2", "Approvals", "UAT-106", ("Build", AMBER_T, AMBER)),
        ("FR-07", "Post approved claim to ERP via API", "Integration", "3", "n/a", "SIT-201", ("Build", AMBER_T, AMBER)),
        ("FR-08", "Daily payment batch file", "Integration", "5", "n/a", "SIT-202", ("Backlog", CANVAS, MUTED)),
        ("FR-09", "Push status notifications", "Functional", "5", "Submitted", "UAT-109", ("Backlog", CANVAS, MUTED)),
        ("BR-07", "Lodging cap by city tier (A ₹7k, B ₹5.5k)", "Business rule", "2", "Review", "UAT-104", ("Done", TEAL_T, TEAL)),
        ("NFR-01", "OCR result in under 4 s (p95)", "Non-functional", "1", "Scan receipt", "PERF-01", ("In test", BLUE_T, BLUE)),
        ("NFR-03", "Role-based access; audit log on approve", "Non-functional", "n/a", "Approvals", "SEC-03", ("Build", AMBER_T, AMBER)),
    ]
    for i, (rid, req, typ, pp, scr, uat, (st, f, col)) in enumerate(rows):
        ry = hy + 50 + i * 56
        s.text(tx + 24, ry, rid, 13, BLUE, 600, font=MONO); s.text(tx + 110, ry, req, 13.5, INK)
        s.text(tx + 520, ry, typ, 12.5, MUTED); s.text(tx + 620, ry, pp, 13, INK)
        s.text(tx + 720, ry, scr, 13, INK); s.text(tx + 880, ry, uat, 13, MUTED, font=MONO)
        pill(s, tx + 1020, ry - 16, st, f, col)
        s.line(tx + 12, ry + 22, tx + tw - 12, ry + 22, "#E6EAF0")
    s.save("06-requirements-rtm.svg")


# ---------------------------------------------------------------- 07 Impact
def impact():
    s = Svg(1440, 900, "07 Impact & KPIs")
    s.header("07 · Outcomes", "Business case and pilot results",
             "8-week pilot with 2 regions (46 claimants) vs 6-month baseline")
    kpis = [("Cycle time", "14.2 d", "3.1 d", "−78%"), ("Claims returned", "31%", "7%", "−24 pts"),
            ("AP minutes per claim", "38", "9", "−76%"), ("Missing receipts", "18%", "2%", "−16 pts")]
    for i, (k, a, b, d) in enumerate(kpis):
        x = 48 + i * 340
        s.rect(x, 160, 320, 170, PAPER, LINE, 10)
        s.text(x + 24, 196, k.upper(), 11, MUTED, 600, ls="1")
        s.text(x + 24, 256, b, 40, INK, 700)
        s.text(x + 24, 290, f"was {a}", 13, MUTED)
        pill(s, x + 210, 236, d, TEAL_T, TEAL, 12)
    # bar chart: cycle time by week
    cx, cy, cw, ch = 48, 370, 860, 440
    s.rect(cx, cy, cw, ch, PAPER, LINE, 10)
    s.text(cx + 24, cy + 36, "Average cycle time by pilot week (working days)", 16, INK, 700)
    vals = [14.2, 11.8, 8.4, 6.0, 4.9, 3.8, 3.4, 3.2, 3.1]
    labels = ["Base", "W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"]
    px0, py0, pw, ph = cx + 70, cy + 80, cw - 110, ch - 140
    for t in [0, 4, 8, 12, 16]:
        yy = py0 + ph - t / 16 * ph
        s.line(px0, yy, px0 + pw, yy, "#E6EAF0"); s.text(px0 - 10, yy + 4, str(t), 11, MUTED, anchor="end")
    bw = pw / len(vals) * 0.6
    for i, v in enumerate(vals):
        bx = px0 + i * pw / len(vals) + (pw / len(vals) - bw) / 2
        bh = v / 16 * ph
        s.rect(bx, py0 + ph - bh, bw, bh, MUTED if i == 0 else BLUE, rx=3)
        s.text(bx + bw / 2, py0 + ph - bh - 8, f"{v}", 11, INK, 600, "middle")
        s.text(bx + bw / 2, py0 + ph + 20, labels[i], 11, MUTED, anchor="middle")
    ty = py0 + ph - 3 / 16 * ph
    s.line(px0, ty, px0 + pw, ty, TEAL, 1.5, "6 4")
    s.line(cx + cw - 150, cy + 31, cx + cw - 124, cy + 31, TEAL, 1.5, "6 4"); s.text(cx + cw - 116, cy + 35, "Target 3.0 d", 12, TEAL, 600)
    # business case
    bx = 948
    s.rect(bx, cy, 444, ch, PAPER, LINE, 10)
    s.text(bx + 24, cy + 36, "Annual business case", 16, INK, 700)
    items = [("AP effort saved", "1,780 h", "₹8.9 L"), ("GST input credit recovered", "", "₹6.2 L"),
             ("Fewer duplicate payments", "", "₹2.1 L"), ("Licence + integration", "", "−₹7.4 L")]
    for i, (a, b, c_) in enumerate(items):
        yy = cy + 86 + i * 52
        s.text(bx + 24, yy, a, 14, INK); s.text(bx + 300, yy, b, 13, MUTED, anchor="end")
        s.text(bx + 420, yy, c_, 14, RED if c_.startswith("−") else INK, 600, "end")
        s.line(bx + 24, yy + 18, bx + 420, yy + 18, "#E6EAF0")
    s.text(bx + 24, cy + 320, "Net annual benefit", 15, INK, 700)
    s.text(bx + 420, cy + 320, "₹9.8 L", 22, TEAL, 700, "end")
    s.text(bx + 24, cy + 350, "Payback: 9 months", 13, MUTED)
    s.text(bx + 24, cy + 400, "All figures are illustrative portfolio data.", 12, MUTED)
    s.save("07-impact-kpis.svg")


if __name__ == "__main__":
    for f in (stakeholders, as_is, to_be, journey, wireframes, requirements, impact):
        f()
    print("\n".join(sorted(p.name for p in OUT.glob("*.svg"))))
