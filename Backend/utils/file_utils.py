def save_proposal(proposal_text: str, filename: str = "proposal_output.txt") -> None:
    """Save the final proposal text to a file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(proposal_text)
    print(f"Proposal saved to: {filename}")