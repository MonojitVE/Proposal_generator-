from core.static_content import contents, company_overview
from core.section_generators import (
    generate_purpose,
    generate_key_deliverables,
    generate_objectives,
    generate_features,
    generate_technical_approach,
    generate_technology_stack,
    generate_future_scope,
    generate_time_budget,
)


def generate_proposal(
    user_input: str,
    user_timeline: str = "",
    user_budget: str = "",
    user_phases: str = "",
    user_resources: str = "",
) -> str:

    # 🔹 Only user context — NO company / contents here
    base_context = f"""
IMPORTANT:
You MUST strictly follow the USER REQUIREMENTS below.
Do NOT assume any domain unless specified.

USER REQUIREMENTS:
{user_input}
"""

    # ── OBJECTIVES ────────────────────────────────────────────────
    print("Generating: Objectives...")
    objective_output = generate_objectives(base_context)

    # ── FEATURES ─────────────────────────────────────────────────
    print("Generating: Features...")
    features_context = f"""
{base_context}

4 OBJECTIVES
{objective_output}
"""
    features_output = generate_features(features_context)

    # ── TECHNICAL APPROACH ───────────────────────────────────────
    print("Generating: Technical Approach...")
    technical_context = f"""
{base_context}

4 OBJECTIVES
{objective_output}

5 FEATURES AND FUNCTIONALITY
{features_output}
"""
    technical_output = generate_technical_approach(technical_context)

    # ── TECH STACK ───────────────────────────────────────────────
    print("Generating: Tech Stack...")
    tech_context = f"""
{base_context}

6 TECHNICAL APPROACH
{technical_output}
"""
    tech_stack_output = generate_technology_stack(tech_context)

    # ── FUTURE SCOPE ─────────────────────────────────────────────
    print("Generating: Future Scope...")
    future_context = f"""
{base_context}

5 FEATURES AND FUNCTIONALITY
{features_output}
"""
    future_scope_output = generate_future_scope(future_context)

    # ── TIME & BUDGET ────────────────────────────────────────────
    print("Generating: Time & Budget...")
    time_budget_output = generate_time_budget(
        user_phases,
        user_timeline,
        user_resources
    )

    # ── PURPOSE ──────────────────────────────────────────────────
    print("Generating: Purpose...")
    purpose_context = f"""
{base_context}

4 OBJECTIVES
{objective_output}

5 FEATURES AND FUNCTIONALITY
{features_output}
"""
    purpose_output = generate_purpose(purpose_context)

    # ── DELIVERABLES ─────────────────────────────────────────────
    print("Generating: Deliverables...")
    deliverables_context = f"""
{base_context}

4 OBJECTIVES
{objective_output}

5 FEATURES AND FUNCTIONALITY
{features_output}
"""
    deliverables_output = generate_key_deliverables(deliverables_context)

    # ── FINAL OUTPUT ─────────────────────────────────────────────
    final_text = f"""
{contents}

{company_overview}

2 PURPOSE OF THE DOCUMENT
{purpose_output}

3 KEY DELIVERABLES
{deliverables_output}

4 OBJECTIVES
{objective_output}

5 FEATURES AND FUNCTIONALITY
{features_output}

6 TECHNICAL APPROACH
{technical_output}

7 TECHNOLOGY STACK
{tech_stack_output}

8 FUTURE SCOPE
{future_scope_output}

{time_budget_output}
"""

    print("\n Proposal generation complete!")
    return final_text