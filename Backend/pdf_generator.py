from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    PageBreak, Table, TableStyle
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import io
import re


# ── Color constants ──────────────────────────────────────────────────────────
BLUE        = colors.HexColor("#1A5FA8")   # "VIRTUAL" part of logo / headings
DARK_NAVY   = colors.HexColor("#1A2B4A")   # "EMPLOYEE" part of logo
ORANGE      = colors.HexColor("#E07820")   # project title on cover
BLACK       = colors.HexColor("#1A1A1A")
DARK_BAR    = colors.HexColor("#1A2B4A")   # the dark banner stripe
WHITE       = colors.white
GRAY        = colors.HexColor("#666666")
LIGHT_GRAY  = colors.HexColor("#F5F5F5")
RULE_BLUE   = colors.HexColor("#D0E0F0")


# ── Page dimensions ──────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4          # 595.27 x 841.89 pts
L_MARGIN = R_MARGIN = 60
CONTENT_W = PAGE_W - L_MARGIN - R_MARGIN   # ~475 pts


# ── Styles ───────────────────────────────────────────────────────────────────
def build_styles():
    return {
        # Cover – big two-tone logo rendered as HTML paragraph
        "logo_line": ParagraphStyle(
            "logo_line",
            fontName="Helvetica-Bold",
            fontSize=36,
            alignment=TA_CENTER,
            leading=44,
        ),
        "logo_tagline": ParagraphStyle(
            "logo_tagline",
            fontName="Helvetica",
            fontSize=11,
            textColor=DARK_NAVY,
            alignment=TA_CENTER,
            leading=16,
        ),
        # "PROPOSAL FOR" label
        "proposal_label": ParagraphStyle(
            "proposal_label",
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=BLUE,
            alignment=TA_CENTER,
            leading=18,
            spaceBefore=30,
            spaceAfter=6,
        ),
        # Orange project title
        "project_title": ParagraphStyle(
            "project_title",
            fontName="Helvetica-Bold",
            fontSize=16,
            textColor=ORANGE,
            alignment=TA_CENTER,
            leading=22,
            spaceAfter=20,
        ),
        # Meta labels (Prepared By / Date)
        "meta_label": ParagraphStyle(
            "meta_label",
            fontName="Helvetica",
            fontSize=11,
            textColor=DARK_NAVY,
            alignment=TA_LEFT,
            leading=20,
        ),
        "meta_value": ParagraphStyle(
            "meta_value",
            fontName="Helvetica",
            fontSize=11,
            textColor=BLUE,
            alignment=TA_LEFT,
            leading=20,
        ),
        # Body content styles
        "section_heading": ParagraphStyle(
            "section_heading",
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=BLUE,
            leading=18,
            spaceBefore=14,
            spaceAfter=4,
        ),
        "numbered_point": ParagraphStyle(
            "numbered_point",
            fontName="Helvetica-Bold",
            fontSize=10,
            textColor=BLACK,
            leading=15,
            spaceBefore=3,
            spaceAfter=2,
            leftIndent=18,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Helvetica",
            fontSize=10,
            textColor=colors.HexColor("#333333"),
            leading=15,
            spaceBefore=2,
            spaceAfter=2,
        ),
    }


# ── Dark banner helper ────────────────────────────────────────────────────────
def dark_banner(width=CONTENT_W, height=18):
    """Returns a full-width dark navy bar (Table with coloured background)."""
    t = Table([["  "]], colWidths=[width], rowHeights=[height])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_BAR),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
    ]))
    return t


# ── Meta row helper ───────────────────────────────────────────────────────────
def meta_table(label: str, value: str, styles, width=CONTENT_W):
    """Returns a two-column table row for Prepared By / Date."""
    t = Table(
        [[Paragraph(label, styles["meta_label"]),
          Paragraph(value, styles["meta_value"])]],
        colWidths=[width * 0.28, width * 0.72],
    )
    t.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
    ]))
    return t


# ── Cover page builder ────────────────────────────────────────────────────────
def build_cover(story, styles, client_name: str, project_title: str, date_str: str):
    """
    Replicates the Image-2 cover layout:
      ① Large top spacer
      ② Two-tone VIRTUAL|EMPLOYEE logo
      ③ Tagline
      ④ "PROPOSAL FOR" label
      ⑤ Orange project title
      ⑥ Dark banner
      ⑦ Prepared By / Date meta rows
      ⑧ Dark banner
      ⑨ PageBreak
    """

    # ① Top spacer – push everything down a bit
    story.append(Spacer(1, 80))

    # ② Two-tone logo  ─  rendered as a single Paragraph with HTML colour spans
    logo_html = (
        f'<font color="#1A5FA8">VIRTUAL</font>'
        f'<font color="#1A2B4A">EMPLOYEE</font>'
    )
    story.append(Paragraph(logo_html, styles["logo_line"]))

    # ③ Tagline removed

    # ④ "PROPOSAL FOR"
    story.append(Spacer(1, 50))
    story.append(Paragraph("PROPOSAL FOR", styles["proposal_label"]))

    # ⑤ Orange project / topic title
    title_text = project_title if project_title else "Project Proposal"
    story.append(Paragraph(title_text, styles["project_title"]))

    # ⑥ Top dark banner
    story.append(Spacer(1, 10))
    story.append(dark_banner())
    story.append(Spacer(1, 16))

    # ⑦ Meta rows
    prepared_by = client_name if client_name else "Virtual Employee Pvt. Ltd."
    story.append(meta_table("Prepared By:", prepared_by, styles))
    story.append(meta_table("Date:", date_str, styles))
    story.append(Spacer(1, 16))

    # ⑧ Bottom dark banner
    story.append(dark_banner())

    # ⑨ Start body content on a fresh page
    story.append(PageBreak())


# ── Line classifier ───────────────────────────────────────────────────────────
SECTION_HEADING_RE = re.compile(
    r"^(\d+\s+[A-Z][A-Z\s&/]+|CONTENTS|COMPANY OVERVIEW|PURPOSE OF THE DOCUMENT|"
    r"KEY DELIVERABLES|OBJECTIVES|FEATURES AND FUNCTIONALITY|TECHNICAL APPROACH|"
    r"TECHNOLOGY STACK|FUTURE SCOPE|TIME AND BUDGET ESTIMATE)$"
)
NUMBERED_POINT_RE = re.compile(r"^\d+[\.\)]\s+.+|^\d+\.\d+[\.\)]?\s+.+")
BULLET_RE = re.compile(r"^[-•\*]\s+.+")


def classify_line(line: str):
    stripped = line.strip()
    if not stripped:
        return "empty", stripped
    if SECTION_HEADING_RE.match(stripped):
        return "heading", stripped
    if NUMBERED_POINT_RE.match(stripped):
        return "numbered", stripped
    if BULLET_RE.match(stripped):
        return "bullet", stripped
    return "body", line.rstrip()


# ── Page-number callback (skips cover page) ───────────────────────────────────
def _make_page_number_cb():
    """
    Returns an onPage callback that draws footer only from page 2 onwards.
    Page 1 = cover → no number.
    """
    def _draw(canvas, doc):
        page_num = canvas.getPageNumber()
        if page_num == 1:          # Cover – no footer
            return
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(GRAY)
        canvas.drawString(L_MARGIN, 30, "VirtualEmployee.com — Confidential")
        canvas.drawRightString(PAGE_W - R_MARGIN, 30, f"Page {page_num - 1}")
        canvas.restoreState()

    return _draw


# ── Main PDF creator ──────────────────────────────────────────────────────────
def create_proposal_pdf(
    proposal_text: str,
    client_name: str = "",
    project_title: str = "",
) -> bytes:
    """
    Parameters
    ----------
    proposal_text : body text of the proposal (plain text with optional markup)
    client_name   : shown as "Prepared By" on the cover  (optional)
    project_title : shown in orange below "PROPOSAL FOR" (optional)
                    – if omitted, falls back to the first non-empty line of
                      proposal_text that looks like a title.
    """
    from datetime import datetime

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=L_MARGIN,
        rightMargin=R_MARGIN,
        topMargin=50,
        bottomMargin=60,
        title="Project Proposal",
        author="VirtualEmployee.com",
    )

    styles = build_styles()
    story  = []

    # Format date as "23rd February 2026" style
    now = datetime.now()
    day = now.day
    suffix = (
        "th" if 11 <= day <= 13
        else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    )
    date_str = f"{day}<super>{suffix}</super> {now.strftime('%B %Y')}."

    # Auto-detect project title from first content line if not supplied
    if not project_title:
        for ln in proposal_text.split("\n"):
            s = ln.strip()
            if s:
                project_title = s
                break

    build_cover(story, styles, client_name, project_title, date_str)

    # ── Render body lines ────────────────────────────────────────────────────
    lines = proposal_text.split("\n")
    for raw_line in lines:
        kind, text = classify_line(raw_line)

        if kind == "empty":
            story.append(Spacer(1, 4))

        elif kind == "heading":
            story.append(Spacer(1, 6))
            story.append(HRFlowable(width="100%", thickness=0.4, color=RULE_BLUE))
            story.append(
                Paragraph(
                    f'<font color="#1A5FA8"><b>{text}</b></font>',
                    styles["section_heading"],
                )
            )

        elif kind == "numbered":
            story.append(Paragraph(text, styles["numbered_point"]))

        elif kind == "bullet":
            clean = re.sub(r"^[-•\*]\s+", "", text)
            story.append(Paragraph(f"• {clean}", styles["numbered_point"]))

        else:
            if text.strip():
                story.append(Paragraph(text.strip(), styles["body"]))

    cb = _make_page_number_cb()
    doc.build(story, onFirstPage=cb, onLaterPages=cb)
    return buffer.getvalue()