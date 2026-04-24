from core.llm_client import call_llm
from prompts.master_prompt import master_prompt
from prompts.section_prompt import (
    d_purposeofdocument_prompts,
    key_deliverables_prompt,
    d_objective,
    d_features_prompts,
    d_technical_approach_prompts,
    d_technology_stack_prompts,
    future_scope_prompt,
    time_budget_prompt,
)


def generate_purpose(previous_output: str) -> str:
    prompt = f"""
{master_prompt}

Previous Content:
{previous_output}

Generate ONLY section:
2 PURPOSE OF THE DOCUMENT

Use the following structured guidance:
{d_purposeofdocument_prompts}
"""
    return call_llm(prompt)


def generate_key_deliverables(previous_output: str) -> str:
    prompt = f"""
{master_prompt}

Previous Content:
{previous_output}

Generate ONLY section:
3 KEY DELIVERABLES

Use the following structured guidance:
{key_deliverables_prompt}
"""
    return call_llm(prompt)


def generate_objectives(previous_output: str) -> str:
    prompt = f"""
{master_prompt}

Previous Content:
{previous_output}

Generate ONLY section:
4 OBJECTIVES

Use the following structured guidance:
{d_objective}

Instructions:
- Return bullet points only
- Select only relevant objectives based on project context
- Do not include all items blindly
"""
    return call_llm(prompt)


def generate_features(previous_output: str) -> str:
    prompt = f"""
{master_prompt}

Previous Content:
{previous_output}

Generate ONLY section:
5 FEATURES AND FUNCTIONALITY

Use the following structured guidance:
{d_features_prompts}
"""
    return call_llm(prompt)


def generate_technical_approach(previous_output: str) -> str:
    prompt = f"""
{master_prompt}

Previous Content:
{previous_output}

Generate ONLY section:
6 TECHNICAL APPROACH
Use the following structured guidance:
{d_technical_approach_prompts}
"""
    return call_llm(prompt)


def generate_technology_stack(previous_output: str) -> str:
    prompt = f"""
{master_prompt}

Previous Content:
{previous_output}

Generate ONLY section:
7 TECHNOLOGY STACK

Use the following structured guidance:
{d_technology_stack_prompts}
"""
    return call_llm(prompt)


def generate_future_scope(previous_output: str) -> str:
    prompt = f"""
{master_prompt}

Previous Content:
{previous_output}

Generate ONLY section:
8 FUTURE SCOPE

Use the following structured guidance:
{future_scope_prompt}
"""
    return call_llm(prompt)


def generate_time_budget(previous_output: str) -> str:
    prompt = f"""
{master_prompt}

Previous Content:
{previous_output}

Generate ONLY section:
9 TIME AND BUDGET ESTIMATE

Use the following structured guidance:
{time_budget_prompt}
"""
    return call_llm(prompt)