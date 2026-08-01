
def _build_refinement_prompt(
    instruction: str,
    existing_competitors: list[str],
    brand_name: str,
) -> str:
    """Build a prompt for refining the competitor list based on user instruction."""
    existing_list = ", ".join(existing_competitors)
    return (
        f"I have a brand called '{brand_name}' and the following competitor list:\n"
        f"{existing_list}\n\n"
        f"User instruction: {instruction}\n\n"
        "Return ONLY the NEW names to add (not the existing ones), one per line, "
        "no numbering, no explanations. If the instruction asks to remove names, "
        "return nothing."
    )

