# from core.llm_client import call_llm
# from prompts.master_prompt import master_prompt
# from prompts.section_prompt import (
#     d_purposeofdocument_prompts,
#     key_deliverables_prompt,
#     d_objective,
#     d_features_prompts,
#     d_technical_approach_prompts,
#     d_technology_stack_prompts,
#     future_scope_prompt,
#     time_budget_prompt,
# )


# def generate_purpose(previous_output: str) -> str:
#     prompt = f"""
# {master_prompt}

# Previous Content:
# {previous_output}

# Generate ONLY section:
# 2 PURPOSE OF THE DOCUMENT

# Use the following structured guidance:
# {d_purposeofdocument_prompts}
# """
#     return call_llm(prompt)


# def generate_key_deliverables(previous_output: str) -> str:
#     prompt = f"""
# {master_prompt}

# Previous Content:
# {previous_output}

# Generate ONLY section:
# 3 KEY DELIVERABLES

# Use the following structured guidance:
# {key_deliverables_prompt}
# """
#     return call_llm(prompt)


# def generate_objectives(previous_output: str) -> str:
#     prompt = f"""
# {master_prompt}

# Previous Content:
# {previous_output}

# Generate ONLY section:
# 4 OBJECTIVES

# Use the following structured guidance:
# {d_objective}

# Instructions:
# - Return bullet points only
# - Select only relevant objectives based on project context
# - Do not include all items blindly
# """
#     return call_llm(prompt)


# def generate_features(previous_output: str) -> str:
#     prompt = f"""
# {master_prompt}

# Previous Content:
# {previous_output}

# Generate ONLY section:
# 5 FEATURES AND FUNCTIONALITY

# Use the following structured guidance:
# {d_features_prompts}
# """
#     return call_llm(prompt)


# def generate_technical_approach(previous_output: str) -> str:
#     prompt = f"""
# {master_prompt}

# Previous Content:
# {previous_output}

# Generate ONLY section:
# 6 TECHNICAL APPROACH
# Use the following structured guidance:
# {d_technical_approach_prompts}
# """
#     return call_llm(prompt)


# def generate_technology_stack(previous_output: str) -> str:
#     prompt = f"""
# {master_prompt}

# Previous Content:
# {previous_output}

# Generate ONLY section:
# 7 TECHNOLOGY STACK

# Use the following structured guidance:
# {d_technology_stack_prompts}
# """
#     return call_llm(prompt)


# def generate_future_scope(previous_output: str) -> str:
#     prompt = f"""
# {master_prompt}

# Previous Content:
# {previous_output}

# Generate ONLY section:
# 8 FUTURE SCOPE

# Use the following structured guidance:
# {future_scope_prompt}
# """
#     return call_llm(prompt)


# def generate_time_budget(user_phases: str = "", user_timeline: str = "", user_resources: str = "") -> str:
#     phases  = user_phases    or "1"
#     timeline = user_timeline or "To be confirmed"
#     resources = user_resources or "To be confirmed"

#     return f"""9 TIME AND BUDGET ESTIMATE

# The entire requirement will be completed in {phases} phase(s) and the Ballpark estimate will be {timeline} (Full Time).

# TOTAL PROJECT TIME: Ballpark estimation will be {timeline} using technologies mentioned, which may vary depending upon the actual complexity and requirements. This duration is based on functionality mentioned in the document.

# NO. OF RESOURCES REQUIRED: {resources}"""


# --------- NEW SECTION_GENERATOR --------------
from core.llm_client import call_llm
from prompts.section_prompt import (
    d_purposeofdocument_prompts,
    key_deliverables_prompt,
    d_objective,
    d_features_prompts,
    d_technical_approach_prompts,
    d_technology_stack_prompts,
    future_scope_prompt,
    workflow_diagram_prompt,
)


# 🔒 COMMON STRICT GUARD
SECTION_GUARD = """
IMPORTANT:
You are generating ONLY ONE section of a proposal.

OUTPUT FORMAT:
- Return clean plain text ONLY
- Do NOT return JSON, code blocks, backticks, or markdown formatting (no **, no ##, no ```)
- Use bullet points with "- " prefix for unordered lists
- Use numbered points like "1. " for ordered items
- For subsections use the format "Label:" on its own line (e.g., "Frontend:", "Backend:")

STRICT RULES:
- Do NOT generate full proposal
- Do NOT include:
  * COMPANY OVERVIEW
  * PURPOSE (unless asked)
  * KEY DELIVERABLES (unless asked)
  * OBJECTIVES (unless asked)
  * FEATURES (unless asked)
  * TECHNICAL APPROACH (unless asked)
  * TECHNOLOGY STACK (unless asked)
  * FUTURE SCOPE (unless asked)
  * TIME & BUDGET
- Do NOT repeat section headings
- Do NOT restart numbering (1,2,3...)

Return ONLY the requested section content.
"""


def generate_purpose(previous_output: str) -> str:
    prompt = f"""
{SECTION_GUARD}

Generate ONLY:
2 PURPOSE OF THE DOCUMENT

Context:
{previous_output}

Instructions:
{d_purposeofdocument_prompts}
"""
    return call_llm(prompt)


def generate_key_deliverables(previous_output: str) -> str:
    prompt = f"""
{SECTION_GUARD}

Generate ONLY:
3 KEY DELIVERABLES

Context:
{previous_output}

Instructions:
{key_deliverables_prompt}

CRITICAL FORMAT RULES:
- Return ONLY a plain text bullet list
- Each deliverable on its own line starting with "- "
- Do NOT use JSON, numbered lists, or nested structures
- Do NOT add any heading or title line

Example output format:
- User Authentication Module
- Admin Dashboard
- Payment Gateway Integration
"""
    return call_llm(prompt)


def generate_objectives(previous_output: str) -> str:
    prompt = f"""
{SECTION_GUARD}

Generate ONLY:
4 OBJECTIVES

Context:
{previous_output}

Instructions:
{d_objective}

CRITICAL FORMAT RULES:
- Return ONLY a plain text bullet list
- Each objective on its own line starting with "- "
- Do NOT use JSON, numbered lists, or nested structures
- Do NOT add any heading or title line
- Select only relevant objectives based on the project context

Example output format:
- Implement secure user authentication and role-based access control
- Build responsive UI optimized for web and mobile platforms
- Integrate third-party payment processing
"""
    return call_llm(prompt)


def generate_features(previous_output: str) -> str:
    prompt = f"""
{SECTION_GUARD}

Generate ONLY:
5 FEATURES AND FUNCTIONALITY

Context:
{previous_output}

Instructions:
{d_features_prompts}

Rules:
- Do NOT repeat the title
- Do NOT generate any other section
"""
    return call_llm(prompt)


def generate_technical_approach(previous_output: str) -> str:
    prompt = f"""
{SECTION_GUARD}

Generate ONLY:
6 TECHNICAL APPROACH

Context:
{previous_output}

Instructions:
{d_technical_approach_prompts}

CRITICAL FORMAT RULES:
- Return clean plain text ONLY (no JSON, no markdown, no code blocks)
- Use subsection labels on their own line followed by a colon
- Under each subsection, use bullet points starting with "- "
- Do NOT add any main heading or title line

Output format MUST be EXACTLY like this:

Overview:
- High-level explanation of the technical approach

Frontend:
- Technology and framework choice
- Key responsibilities

Backend:
- Architecture and framework
- API design approach

Database:
- Database choice and reasoning
- Data modeling approach

Architecture:
- System architecture overview
- Scalability considerations

Integrations:
- Third-party services
- API integrations

Security:
- Authentication approach
- Data protection

DevOps:
- Deployment strategy
- CI/CD approach

Workflow:
- Step-by-step development flow
"""
    return call_llm(prompt)


def generate_technology_stack(previous_output: str) -> str:
    prompt = f"""
{SECTION_GUARD}

Generate ONLY:
7 TECHNOLOGY STACK

Context:
{previous_output}

Instructions:
{d_technology_stack_prompts}

CRITICAL: You MUST format the output as a Markdown table exactly like this:
| Category | Technology |
|---|---|
| Frontend | React |
"""
    return call_llm(prompt)


def generate_future_scope(previous_output: str) -> str:
    prompt = f"""
{SECTION_GUARD}

Generate ONLY:
9 FUTURE SCOPE

Context:
{previous_output}

Instructions:
{future_scope_prompt}
"""
    return call_llm(prompt)


def generate_workflow_diagram(previous_output: str) -> str:
    prompt = f"""
You are generating ONLY ONE section of a proposal: a Mermaid workflow diagram.

STRICT RULES:
- Do NOT generate a full proposal
- Do NOT include any other sections (Company Overview, Purpose, Objectives, etc.)
- Return ONLY the mermaid diagram wrapped in triple backticks

Generate ONLY:
8 WORKFLOW DIAGRAM

Context:
{previous_output}

Instructions:
{workflow_diagram_prompt}

CRITICAL: You MUST wrap the diagram in triple backticks with 'mermaid' like this:
```mermaid
flowchart TD
...
```

Return ONLY the mermaid code block. Nothing else.
"""
    return call_llm(prompt)


# ── Timeline key → human-readable label mapping ─────────────────────────────
TIMELINE_LABELS = {
    "1_month":      "< 1 Month",
    "1_3_months":   "1 – 3 Months",
    "3_6_months":   "3 – 6 Months",
    "6_12_months":  "6 – 12 Months",
    "12_plus":      "12+ Months",
}

# ── Timeline key → approximate (min, max) month ranges for splitting ─────────
TIMELINE_MONTHS = {
    "1_month":      (0.5, 1.0),
    "1_3_months":   (1.0, 3.0),
    "3_6_months":   (3.0, 6.0),
    "6_12_months":  (6.0, 12.0),
    "12_plus":      (12.0, 18.0),
}


def _format_duration(lo: float, hi: float) -> str:
    """Format month numbers into a clean, human-readable duration (Weeks or Months)."""
    def _clean(val: float) -> float:
        rounded_int = round(val)
        if abs(val - rounded_int) <= 0.15:
            return float(rounded_int)
        return round(val * 2) / 2

    c_lo = _clean(lo)
    c_hi = _clean(hi)
    if c_lo > c_hi:
        c_lo = c_hi

    # If upper bound is under ~1 month, express in weeks
    if c_hi <= 0.8:
        lo_w = max(1, round(lo * 4.3))
        hi_w = max(1, round(hi * 4.3))
        if lo_w == hi_w:
            unit = "Week" if lo_w == 1 else "Weeks"
            return f"~{lo_w} {unit}"
        return f"~{lo_w} – {hi_w} Weeks"

    def _fmt(v: float) -> str:
        return str(int(v)) if v == int(v) else f"{v:g}"

    if c_lo == c_hi:
        unit = "Month" if c_lo == 1 else "Months"
        return f"~{_fmt(c_lo)} {unit}"
    return f"~{_fmt(c_lo)} – {_fmt(c_hi)} Months"


def _parse_custom_phases(phases_input: str):
    """
    Parse user phases input.
    Can be a number ('2', '3'), or a text description like:
    'Phase 1: Discovery (2 weeks) -> Phase 2: MVP -> Phase 3: QA'
    """
    import re
    if not phases_input or not phases_input.strip():
        return None, 1

    text = phases_input.strip()

    # Check if it's just a single integer
    if text.isdigit():
        return None, max(1, int(text))

    # Check if user specified custom phases with delimiters (-> , \n , ;)
    items = re.split(r"[\n;]|(?:\s*(?:->|→)\s*)", text)
    cleaned_phases = []
    for item in items:
        item_str = item.strip()
        if item_str:
            # Clean up leading numbers or 'Phase X:' prefixes if present
            cleaned = re.sub(r"^(?:phase\s*\d+[\s:\-—]+|\d+[\.\)]\s*)", "", item_str, flags=re.IGNORECASE).strip()
            if cleaned:
                cleaned_phases.append(cleaned)

    if cleaned_phases:
        return cleaned_phases, len(cleaned_phases)

    return None, 1


def generate_time_budget(
    user_phases: str = "",
    user_timeline: str = "",
    user_resources: str = ""
) -> str:
    """
    Generates an intelligent, realistic, and project-tailored Time and Budget section.
    - If user provided a timeline: intelligently divides the duration realistically across phases.
    - If user did NOT provide a timeline: marks timeline and phase durations as 'To be confirmed'.
    """
    import re

    # 1. Parse user timeline
    timeline_key = user_timeline.strip() if user_timeline else ""
    month_range = TIMELINE_MONTHS.get(timeline_key)

    if timeline_key:
        timeline_label = TIMELINE_LABELS.get(timeline_key, timeline_key)
        # Try to parse if user entered a custom duration like "6 weeks" or "4 months"
        if not month_range:
            weeks_match = re.search(r"(\d+)\s*(?:-\s*(\d+))?\s*weeks?", timeline_key, re.IGNORECASE)
            months_match = re.search(r"(\d+)\s*(?:-\s*(\d+))?\s*months?", timeline_key, re.IGNORECASE)
            if weeks_match:
                w_lo = float(weeks_match.group(1)) / 4.3
                w_hi = float(weeks_match.group(2)) / 4.3 if weeks_match.group(2) else w_lo
                month_range = (w_lo, w_hi)
            elif months_match:
                m_lo = float(months_match.group(1))
                m_hi = float(months_match.group(2)) if months_match.group(2) else m_lo
                month_range = (m_lo, m_hi)
    else:
        timeline_label = "To be confirmed"
        month_range = None

    # 2. Parse user phases
    custom_phase_names, num_phases = _parse_custom_phases(user_phases)

    # 3. Determine realistic phase titles
    default_phase_catalog = {
        1: [
            "Phase 1 — Core Development, QA & Production Launch"
        ],
        2: [
            "Phase 1 — Discovery, UI/UX Design & Architecture",
            "Phase 2 — Core Development, Integrations & Launch"
        ],
        3: [
            "Phase 1 — Discovery, UI/UX Design & Architecture",
            "Phase 2 — Core Engine & Module Development",
            "Phase 3 — Integrations, QA & Production Deployment"
        ],
        4: [
            "Phase 1 — Requirements & UI/UX Design",
            "Phase 2 — Backend Architecture & Core Services",
            "Phase 3 — Frontend Integration & Workflows",
            "Phase 4 — Security, UAT & Production Launch"
        ]
    }

    if custom_phase_names:
        phase_titles = [f"Phase {i + 1} — {name}" for i, name in enumerate(custom_phase_names)]
    else:
        phase_titles = default_phase_catalog.get(
            num_phases,
            [f"Phase {i} — Module & Feature Development" for i in range(1, num_phases + 1)]
        )

    # 4. Determine realistic proportional distribution
    # (Discovery/Design: ~20-25%, Core Development: ~50-60%, Testing/Launch: ~20-25%)
    if num_phases == 1:
        ratios = [1.0]
    elif num_phases == 2:
        ratios = [0.35, 0.65]
    elif num_phases == 3:
        ratios = [0.25, 0.50, 0.25]
    elif num_phases == 4:
        ratios = [0.20, 0.35, 0.25, 0.20]
    else:
        ratios = [1.0 / num_phases] * num_phases

    # 5. Build table rows
    table_rows = ""
    if month_range:
        total_lo, total_hi = month_range
        for i, title in enumerate(phase_titles):
            p_lo = round(total_lo * ratios[i], 1)
            p_hi = round(total_hi * ratios[i], 1)
            p_lo = max(0.25, p_lo)
            p_hi = max(p_lo, p_hi)
            phase_duration = _format_duration(p_lo, p_hi)
            table_rows += f"| {title} | {phase_duration} |\n"
    else:
        for title in phase_titles:
            table_rows += f"| {title} | To be confirmed |\n"

    resources = user_resources.strip() if user_resources and user_resources.strip() else "To be confirmed"

    return f"""The entire requirement will be completed in {num_phases} phase(s) and the Ballpark estimate will be {timeline_label} (Full Time).

| PHASE | DURATION |
|---|---|
{table_rows}| **Total Estimated Timeline** | **{timeline_label}** |

NO. OF RESOURCES REQUIRED: {resources}"""