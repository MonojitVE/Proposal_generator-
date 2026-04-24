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
    """
    Main pipeline: generates a full proposal section by section.
    Purpose of Document and Key Deliverables are generated LAST so they
    have full context of the entire proposal, then inserted into their
    correct positions in the final output.

    Parameters
    ----------
    user_input : str
        Short or detailed project description from the user.
    user_timeline : str
        Timeline directly from user input (not LLM-generated).
    user_budget : str
        Budget directly from user input (not LLM-generated).
    user_phases : str
        Number of phases directly from user input (not LLM-generated).
    user_resources : str
        Resources directly from user input (not LLM-generated).

    Returns
    -------
    str
        Complete formatted proposal as plain text.
    """

    base = f"""{contents}\n\n{company_overview}

    IMPORTANT:
You MUST strictly follow the USER REQUIREMENTS below.
Do NOT assume any domain unless specified.

    USER REQUIREMENTS:
{user_input}
"""

    # ── Section 4: Objectives ────────────────────────────────────────────────
    print("Generating: Objectives...")
    previous = base
    objective_output = generate_objectives(previous)

    # ── Section 5: Features and Functionality ────────────────────────────────
    print("Generating: Features and Functionality...")
    previous = f"""
{base}

4 OBJECTIVES
{objective_output}
"""
    features_output = generate_features(previous)

    # ── Section 6: Technical Approach ────────────────────────────────────────
    print("Generating: Technical Approach...")
    previous = f"""
{base}

4 OBJECTIVES
{objective_output}

5 FEATURES AND FUNCTIONALITY
{features_output}
"""
    technical_output = generate_technical_approach(previous)

    # ── Section 7: Technology Stack ──────────────────────────────────────────
    print("Generating: Technology Stack...")
    previous = f"""
{base}

4 OBJECTIVES
{objective_output}

5 FEATURES AND FUNCTIONALITY
{features_output}

6 TECHNICAL APPROACH
{technical_output}
"""
    tech_stack_output = generate_technology_stack(previous)

    # ── Section 8: Future Scope ──────────────────────────────────────────────
    print("Generating: Future Scope...")
    previous = f"""
{base}

4 OBJECTIVES
{objective_output}

5 FEATURES AND FUNCTIONALITY
{features_output}

6 TECHNICAL APPROACH
{technical_output}

7 TECHNOLOGY STACK
{tech_stack_output}
"""
    future_scope_output = generate_future_scope(previous)

    # ── Section 9: Time and Budget Estimate (user input, no LLM) ─────────────
    print("Generating: Time and Budget Estimate...")
    time_budget_output = generate_time_budget(user_phases, user_timeline, user_resources)

    # ── Full context for purpose + deliverables ──────────────────────────────
    full_context = f"""
{base}

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

9 TIME AND BUDGET ESTIMATE
{time_budget_output}
"""

    # ── Section 2: Purpose of Document (generated with full context) ─────────
    print("Generating: Purpose of Document...")
    purpose_output = generate_purpose(full_context)

    # ── Section 3: Key Deliverables (generated with full context) ────────────
    print("Generating: Key Deliverables...")
    previous = f"""
{full_context}

2 PURPOSE OF THE DOCUMENT
{purpose_output}
"""
    deliverables_output = generate_key_deliverables(previous)

    # ── Assemble Final Proposal ──────────────────────────────────────────────
    final_text = f"""
{contents}

{company_overview}

{purpose_output}

3 KEY DELIVERABLES
{deliverables_output}

{objective_output}

{features_output}

{technical_output}

7 TECHNOLOGY STACK
{tech_stack_output}

8 FUTURE SCOPE
{future_scope_output}

{time_budget_output}
"""

    print("\nProposal generation complete!")
    return final_text