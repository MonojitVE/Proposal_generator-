import { jsPDF } from "jspdf";

const BLUE = "#2980B9";
const ORANGE = "#E8962A";
const DARK = "#2C3E50";
const MID = "#555E6D";
const RULE = "#CCCCCC";

const PAGE_W = 210;
const PAGE_H = 297;
const ML = 18;
const MR = 18;
const CW = PAGE_W - ML - MR;

function hexRgb(hex) {
  const h = hex.replace("#", "");
  return [
    parseInt(h.slice(0, 2), 16),
    parseInt(h.slice(2, 4), 16),
    parseInt(h.slice(4, 6), 16),
  ];
}
function sc(doc, hex, type = "text") {
  const [r, g, b] = hexRgb(hex);
  type === "text" ? doc.setTextColor(r, g, b) : doc.setFillColor(r, g, b);
}
function sd(doc, hex) {
  const [r, g, b] = hexRgb(hex);
  doc.setDrawColor(r, g, b);
}
function tw(doc, text) {
  return (
    (doc.getStringUnitWidth(text) * doc.getFontSize()) /
    doc.internal.scaleFactor
  );
}
function wrap(doc, text, maxW, size) {
  doc.setFontSize(size);
  return doc.splitTextToSize(text, maxW);
}

function drawHeader(doc) {
  doc.setFontSize(9);
  doc.setFont("helvetica", "bold");
  sc(doc, BLUE);
  const vw = tw(doc, "VIRTUAL");
  doc.text("VIRTUAL", ML, 13);
  sc(doc, DARK);
  doc.text("EMPLOYEE", ML + vw, 13);

  doc.setFontSize(6.5);
  doc.setFont("helvetica", "normal");
  sc(doc, MID);
  doc.text("• 1st Online Employee Supermarket •", ML + 1, 17);

  sd(doc, RULE);
  doc.setLineWidth(0.3);
  doc.line(ML, 19, PAGE_W - MR, 19);
}

function drawCover(doc, { projectTitle, preparedBy, date }) {
  doc.setFontSize(36);
  doc.setFont("helvetica", "bold");
  const vw = tw(doc, "VIRTUAL");
  const ew = tw(doc, "EMPLOYEE");
  const logoX = (PAGE_W - vw - ew) / 2;

  sc(doc, BLUE);
  doc.text("VIRTUAL", logoX, 60);
  sc(doc, DARK);
  doc.text("EMPLOYEE", logoX + vw, 60);

  doc.setFontSize(10);
  doc.setFont("helvetica", "normal");
  sc(doc, MID);
  const tag = "• 1st Online Employee Supermarket •";
  doc.text(tag, (PAGE_W - tw(doc, tag)) / 2, 70);

  doc.setFontSize(15);
  doc.setFont("helvetica", "bold");
  sc(doc, BLUE);
  const pf = "PROPOSAL FOR";
  doc.text(pf, (PAGE_W - tw(doc, pf)) / 2, 115);

  doc.setFontSize(16);
  doc.setFont("helvetica", "bold");
  sc(doc, ORANGE);
  const titleLines = wrap(doc, projectTitle, CW - 10, 16);
  let ty = 128;
  titleLines.forEach((line) => {
    doc.text(line, (PAGE_W - tw(doc, line)) / 2, ty);
    ty += 9;
  });

  doc.setFillColor(0, 0, 0);
  doc.rect(ML, ty + 5, CW, 7, "F");

  const infoY = ty + 22;
  doc.setFontSize(10.5);
  doc.setFont("helvetica", "normal");
  sc(doc, DARK);
  doc.text("Prepared By:", ML + 18, infoY);
  sc(doc, BLUE);
  doc.text(preparedBy || "—", ML + 55, infoY);

  sc(doc, DARK);
  doc.text("Date:", ML + 18, infoY + 10);
  sc(doc, BLUE);
  doc.text(
    date ||
      new Date().toLocaleDateString("en-GB", {
        day: "numeric",
        month: "long",
        year: "numeric",
      }),
    ML + 55,
    infoY + 10,
  );

  doc.setFillColor(0, 0, 0);
  doc.rect(ML, infoY + 16, CW, 7, "F");
}

const H1_RE = /^(\d+)\s+([A-Z][A-Z\s&/,]+)$/;
const BULLET_RE = /^[-•*]\s+/;
const SUBHEAD_RE = /^([A-Z][\.\)]\s+.+|\d+[\.\)]\s+[A-Z].+)/;

function parseLines(text) {
  return text.split("\n").map((raw) => {
    const t = raw.trim();
    if (!t) return { kind: "empty" };
    if (H1_RE.test(t)) {
      const [, num, title] = t.match(H1_RE);
      return { kind: "h1", num, title };
    }
    if (BULLET_RE.test(t))
      return { kind: "bullet", text: t.replace(/^[-•*]\s+/, "") };
    if (SUBHEAD_RE.test(t)) return { kind: "sub", text: t };
    return { kind: "body", text: t };
  });
}

function drawTOC(doc, sections) {
  drawHeader(doc);
  let y = 30;

  doc.setFontSize(18);
  doc.setFont("helvetica", "bold");
  sc(doc, BLUE);
  doc.text("Contents", ML, y);
  y += 10;

  sections.forEach(({ num, title, page, indent }) => {
    const isMajor = indent === 0;
    const fontSize = isMajor ? 10.5 : 9.5;
    const fontStyle = isMajor ? "bold" : "normal";
    const x = ML + indent;
    const maxW = CW - indent - 12;

    doc.setFontSize(fontSize);
    doc.setFont("helvetica", fontStyle);
    sc(doc, DARK);

    const label = num ? `${num}  ${title}` : title;
    const titleWrapped = doc.splitTextToSize(label, maxW);

    if (y + titleWrapped.length * 5.2 > PAGE_H - 18) {
      doc.addPage();
      drawHeader(doc);
      y = 30;
    }

    titleWrapped.forEach((line, li) => doc.text(line, x, y + li * 5.2));
    doc.text(String(page), PAGE_W - MR, y, { align: "right" });
    y += titleWrapped.length * 5.2 + (isMajor ? 1.5 : 0.8);
  });
}

export async function generateProposalPdf(
  proposalText,
  {
    projectTitle = "Project Proposal",
    preparedBy = "",
    clientName = "",
    date = "",
  } = {},
) {
  const doc = new jsPDF({ unit: "mm", format: "a4" });
  doc.setFont("helvetica");

  // ── Strip any CONTENTS block the backend included ─────────────────────────
  // Removes "CONTENTS" heading + everything after it until first numbered section
  const cleaned = proposalText.replace(
    /(\n|^)(CONTENTS|\d+\s+CONTENTS)[^\n]*\n([\s\S]*?)(?=(\n|^)\d+\s+[A-Z][A-Z])/gm,
    "\n",
  );

  const parsed = parseLines(cleaned);
  const PAGE_BOTTOM = PAGE_H - 18;

  // ── Dry run to get TOC page numbers ───────────────────────────────────────
  let simPage = 3; // 1=cover, 2=TOC, 3+=content
  let simY = 26;
  const tocEntries = [];

  function simBreak(n) {
    if (simY + n > PAGE_BOTTOM) {
      simPage++;
      simY = 26;
    }
  }

  for (const e of parsed) {
    switch (e.kind) {
      case "empty":
        simY += 2;
        break;
      case "h1":
        simBreak(14);
        simY += 5;
        tocEntries.push({
          num: e.num,
          title: e.title,
          page: simPage,
          indent: 0,
        });
        simY += 6;
        break;
      case "sub":
        simBreak(8);
        simY += 2;
        tocEntries.push({ num: "", title: e.text, page: simPage, indent: 8 });
        simY += 6;
        break;
      case "bullet": {
        const n = Math.ceil(e.text.length / 80) || 1;
        simBreak(n * 4.8 + 2);
        simY += n * 4.8 + 1;
        break;
      }
      case "body": {
        const n = Math.ceil(e.text.length / 90) || 1;
        simBreak(n * 4.8 + 2);
        simY += n * 4.8 + 2;
        break;
      }
    }
  }

  // ── Page 1: Cover ─────────────────────────────────────────────────────────
  drawCover(doc, { projectTitle, preparedBy, date });

  // ── Page 2: TOC ───────────────────────────────────────────────────────────
  doc.addPage();
  drawTOC(doc, tocEntries);

  // ── Page 3+: Content ──────────────────────────────────────────────────────
  doc.addPage();
  drawHeader(doc);
  let y = 26;

  function pageBreak(n = 10) {
    if (y + n > PAGE_BOTTOM) {
      doc.addPage();
      drawHeader(doc);
      y = 26;
    }
  }
  function rule() {
    pageBreak(5);
    sd(doc, RULE);
    doc.setLineWidth(0.25);
    doc.line(ML, y, PAGE_W - MR, y);
    y += 4;
  }

  for (const e of parsed) {
    switch (e.kind) {
      case "empty":
        y += 2;
        break;

      case "h1":
        pageBreak(14);
        y += 5;
        doc.setFontSize(12);
        doc.setFont("helvetica", "bold");
        sc(doc, BLUE);
        doc.text(`${e.num}  ${e.title}`, ML, y);
        y += 2;
        rule();
        break;

      case "sub": {
        pageBreak(8);
        y += 2;
        doc.setFontSize(10);
        doc.setFont("helvetica", "bold");
        sc(doc, DARK);
        const wl = wrap(doc, e.text, CW - 4, 10);
        wl.forEach((line, li) => doc.text(line, ML + 2, y + li * 5));
        y += wl.length * 5 + 1;
        break;
      }

      case "bullet": {
        const wl = wrap(doc, e.text, CW - 8, 10);
        pageBreak(wl.length * 4.8 + 2);
        doc.setFontSize(10);
        doc.setFont("helvetica", "normal");
        sc(doc, DARK);
        const [r, g, b] = hexRgb(DARK);
        doc.setFillColor(r, g, b);
        doc.circle(ML + 2.2, y - 1.4, 0.8, "F");
        wl.forEach((line, li) => doc.text(line, ML + 5, y + li * 4.8));
        y += wl.length * 4.8 + 1;
        break;
      }

      case "body": {
        doc.setFontSize(10);
        doc.setFont("helvetica", "normal");
        sc(doc, DARK);
        const wl = wrap(doc, e.text, CW, 10);
        pageBreak(wl.length * 4.8 + 2);
        wl.forEach((line, li) => doc.text(line, ML, y + li * 4.8));
        y += wl.length * 4.8 + 2;
        break;
      }
    }
  }

  // ── Footers ───────────────────────────────────────────────────────────────
  const total = doc.getNumberOfPages();
  for (let p = 2; p <= total; p++) {
    doc.setPage(p);
    doc.setFontSize(8);
    doc.setFont("helvetica", "normal");
    sc(doc, MID);
    if (clientName) doc.text(`Prepared for: ${clientName}`, ML, PAGE_H - 8);
    if (p >= 3)
      doc.text(String(p - 2), PAGE_W / 2, PAGE_H - 8, { align: "center" });
    if (preparedBy)
      doc.text(preparedBy, PAGE_W - MR, PAGE_H - 8, { align: "right" });
  }

  return doc.output("blob");
}
