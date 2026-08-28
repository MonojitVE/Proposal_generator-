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
    "1_month":      (0.5, 1),
    "1_3_months":   (1, 3),
    "3_6_months":   (3, 6),
    "6_12_months":  (6, 12),
    "12_plus":      (12, 18),
}


def _format_month_range(lo: float, hi: float) -> str:
    """Format a (lo, hi) month range into a readable duration string."""
    def _fmt(v: float) -> str:
        return str(int(v)) if v == int(v) else f"{v:.1f}"

    if lo == hi:
        unit = "Month" if lo == 1 else "Months"
        return f"~{_fmt(lo)} {unit}"
    return f"~{_fmt(lo)} – {_fmt(hi)} Months"


def generate_time_budget(
    user_phases: str = "",
    user_timeline: str = "",
    user_resources: str = ""
) -> str:
    phases = user_phases or "1"
    resources = user_resources or "To be confirmed"

    # Resolve the human-readable timeline label
    # If the value is a known key (from the frontend dropdown), map it;
    # otherwise treat it as free text and use as-is.
    timeline_key = user_timeline.strip() if user_timeline else ""
    timeline_label = TIMELINE_LABELS.get(timeline_key, timeline_key) or "To be confirmed"

    # Attempt to parse phases as integer, default to 1
    try:
        num_phases = int(phases)
    except ValueError:
        num_phases = 1

    # Calculate per-phase durations if we have a known timeline range
    month_range = TIMELINE_MONTHS.get(timeline_key)

    table_rows = ""
    if month_range and num_phases > 0:
        total_lo, total_hi = month_range
        phase_lo = round(total_lo / num_phases, 1)
        phase_hi = round(total_hi / num_phases, 1)
        phase_duration = _format_month_range(phase_lo, phase_hi)

        for i in range(1, num_phases + 1):
            table_rows += f"| Phase {i} — Development | {phase_duration} |\n"
    else:
        # No computable range — fall back to "To be confirmed" per phase
        for i in range(1, num_phases + 1):
            table_rows += f"| Phase {i} — Development | To be confirmed |\n"

    return f"""The entire requirement will be completed in {phases} phase(s) and the Ballpark estimate will be {timeline_label} (Full Time).

| PHASE | DURATION |
|---|---|
{table_rows}| **Total Estimated Timeline** | **{timeline_label}** |

NO. OF RESOURCES REQUIRED: {resources}"""