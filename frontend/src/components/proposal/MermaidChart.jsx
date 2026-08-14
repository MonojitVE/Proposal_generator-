import React, { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';

mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose',
});

/**
 * Sanitize LLM-generated mermaid code to fix common parse errors.
 * Wraps node labels in quotes when they contain special characters
 * like parentheses that Mermaid would misinterpret as shape delimiters.
 */
function sanitizeMermaidCode(code) {
  return code
    // [Label (something)] → ["Label (something)"]
    .replace(/\[([^\]"]*[()][^\]"]*)\]/g, '["$1"]')
    // {Label (something)} → {"Label (something)"}
    .replace(/\{([^}"]*[()][^}"]*)\}/g, '{"$1"}');
}

export default function MermaidChart({ chart }) {
  const chartRef = useRef(null);
  const [svgContent, setSvgContent] = useState('');
  const [error, setError] = useState(false);

  useEffect(() => {
    let isMounted = true;
    
    if (chart && chartRef.current) {
      const renderChart = async () => {
        try {
          const id = `mermaid-${Math.random().toString(36).substr(2, 9)}`;
          const sanitized = sanitizeMermaidCode(chart);
          const { svg } = await mermaid.render(id, sanitized);
          if (isMounted) {
            setSvgContent(svg);
            setError(false);
          }
        } catch (err) {
          console.error('Mermaid rendering failed', err);
          if (isMounted) {
            setError(true);
          }
        }
      };
      renderChart();
    }
    
    return () => {
      isMounted = false;
    };
  }, [chart]);

  if (error) {
    return <div className="mermaid-error" style={{ color: 'red', padding: '10px', border: '1px solid red' }}>Failed to render diagram</div>;
  }

  return (
    <div
      ref={chartRef}
      className="mermaid-wrapper"
      dangerouslySetInnerHTML={{ __html: svgContent }}
      style={{ display: 'flex', justifyContent: 'center', margin: '20px 0', overflowX: 'auto' }}
    />
  );
}
