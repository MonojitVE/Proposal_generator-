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
)


# 🔒 COMMON STRICT GUARD
SECTION_GUARD = """
IMPORTANT:
You are generating ONLY ONE section of a proposal.

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

Rules:
- Return ONLY bullet points
- Do NOT add headings
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

Output format MUST be:

Overview:
...

Frontend:
...

Backend:
...

Database:
...

Architecture:
...

Integrations:
...

Security:
...

DevOps:
...

Workflow:
...
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
"""
    return call_llm(prompt)


def generate_future_scope(previous_output: str) -> str:
    prompt = f"""
{SECTION_GUARD}

Generate ONLY:
8 FUTURE SCOPE

Context:
{previous_output}

Instructions:
{future_scope_prompt}
"""
    return call_llm(prompt)


def generate_time_budget(
    user_phases: str = "",
    user_timeline: str = "",
    user_resources: str = ""
) -> str:
    phases = user_phases or "1"
    timeline = user_timeline or "To be confirmed"
    resources = user_resources or "To be confirmed"

    return f"""9 TIME AND BUDGET ESTIMATE

The entire requirement will be completed in {phases} phase(s) and the Ballpark estimate will be {timeline} (Full Time).

TOTAL PROJECT TIME: Ballpark estimation will be {timeline} using technologies mentioned, which may vary depending upon the actual complexity and requirements. This duration is based on functionality mentioned in the document.

NO. OF RESOURCES REQUIRED: {resources}"""