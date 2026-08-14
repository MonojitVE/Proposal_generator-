import { useMemo } from 'react';
import './ProposalViewer.css';

// Section headings the backend produces (mirrors pdf_generator.py SECTION_HEADING_RE)
const HEADING_PATTERNS = [
  /^\d+\s+[A-Z][A-Z\s&/]+$/,
  /^CONTENTS$/i,
  /^COMPANY OVERVIEW$/i,
  /^PURPOSE OF THE DOCUMENT$/i,
  /^KEY DELIVERABLES$/i,
  /^OBJECTIVES$/i,
  /^FEATURES AND FUNCTIONALITY$/i,
  /^TECHNICAL APPROACH$/i,
  /^TECHNOLOGY STACK$/i,
  /^WORKFLOW DIAGRAM$/i,
  /^FUTURE SCOPE$/i,
  /^TIME AND BUDGET ESTIMATE$/i,
  /^PURPOSE$/i,
  /^DELIVERABLES$/i,
];

const SUBSECTION_RE = /^(Frontend|Backend|Database|Architecture|Integrations|Security|DevOps|Workflow|Overview|Timeline|Phases|Budget|Other Tools|System Architecture|Testing|Deployment|Monitoring|Authentication|Requirement Analysis|Post[- ]?Launch|Infrastructure|Caching|Real[- ]?Time|Offline|Storage|AI|Automation|Scalability|Performance|Error Handling):\s*/i;
const NUMBERED_RE   = /^\d+[\.\)]\s+.+|^\d+\.\d+[\.\)]?\s+.+/;
const BULLET_RE     = /^[-•*●]\s+.+/;

function isHeading(line) {
  return HEADING_PATTERNS.some(p => p.test(line.trim()));
}

function classifyLine(raw) {
  const stripped = raw.trim();
  if (!stripped) return { kind: 'empty', text: '' };
  if (isHeading(stripped)) return { kind: 'heading', text: stripped };
  if (SUBSECTION_RE.test(stripped)) return { kind: 'subsection', text: stripped };
  if (NUMBERED_RE.test(stripped)) return { kind: 'numbered', text: stripped };
  if (BULLET_RE.test(stripped)) return { kind: 'bullet', text: stripped.replace(/^[-•*●]\s+/, '') };
  return { kind: 'body', text: stripped };
}

import MermaidChart from './MermaidChart';

function parseProposal(text) {
  const rawLines = text.split('\n');
  const blocks = [];
  
  let i = 0;
  while (i < rawLines.length) {
    const raw = rawLines[i];
    const stripped = raw.trim();

    // Check for mermaid block
    if (stripped.startsWith('```mermaid')) {
      let chartText = '';
      i++;
      while (i < rawLines.length && !rawLines[i].trim().startsWith('```')) {
        chartText += rawLines[i] + '\n';
        i++;
      }
      blocks.push({ kind: 'mermaid', text: chartText.trim(), key: `mermaid-${i}` });
      i++;
      continue;
    }

    // Check for table block
    if (stripped.startsWith('|') && stripped.endsWith('|')) {
      const tableLines = [];
      while (i < rawLines.length && rawLines[i].trim().startsWith('|') && rawLines[i].trim().endsWith('|')) {
        tableLines.push(rawLines[i].trim());
        i++;
      }
      
      const rows = tableLines.map(line => 
        line.split('|').slice(1, -1).map(cell => cell.trim())
      );
      
      // Assume row 0 is header, row 1 is separator (---|---), row 2+ are data
      if (rows.length >= 2 && rows[1].every(cell => cell.match(/^[-:]+$/))) {
        blocks.push({ 
          kind: 'table', 
          headers: rows[0], 
          data: rows.slice(2), 
          key: `table-${i}` 
        });
      } else {
        // Fallback if it doesn't look like a valid markdown table
        tableLines.forEach((tLine, idx) => {
          blocks.push({ ...classifyLine(tLine), key: `table-fallback-${i}-${idx}` });
        });
      }
      continue;
    }

    // Regular line processing
    blocks.push({ ...classifyLine(raw), key: `line-${i}` });
    i++;
  }
  
  return blocks;
}

export default function ProposalViewer({ text }) {
  const blocks = useMemo(() => parseProposal(text), [text]);

  return (
    <div className="pv">
      {blocks.map(({ kind, text, key, headers, data }) => {
        if (kind === 'empty') return <div key={key} className="pv__spacer" />;
        if (kind === 'heading') return (
          <div key={key} className="pv__heading-wrap">
            <h2 className="pv__heading">{text}</h2>
            <div className="pv__heading-rule" />
          </div>
        );
        if (kind === 'subsection') return (
          <h3 key={key} className="pv__subsection">{text}</h3>
        );
        if (kind === 'numbered') return (
          <p key={key} className="pv__numbered">{text}</p>
        );
        if (kind === 'bullet') return (
          <div key={key} className="pv__bullet">
            <span className="pv__bullet-dot" aria-hidden="true" />
            <span>{text}</span>
          </div>
        );
        if (kind === 'mermaid') return (
          <MermaidChart key={key} chart={text} />
        );
        if (kind === 'table') return (
          <div key={key} className="pv__table-container">
            <table className="pv__table">
              <thead>
                <tr>
                  {headers.map((h, idx) => (
                    <th key={idx}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.map((row, rIdx) => (
                  <tr key={rIdx}>
                    {row.map((cell, cIdx) => {
                      // Check for markdown bold (**text**) in cell
                      const boldMatch = cell.match(/\*\*(.+?)\*\*/);
                      return (
                        <td key={cIdx}>
                          {boldMatch ? (
                            <>
                              {cell.substring(0, boldMatch.index)}
                              <strong>{boldMatch[1]}</strong>
                              {cell.substring(boldMatch.index + boldMatch[0].length)}
                            </>
                          ) : cell}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
        return <p key={key} className="pv__body">{text}</p>;
      })}
    </div>
  );
}
