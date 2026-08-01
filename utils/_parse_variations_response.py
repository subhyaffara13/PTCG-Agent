
def _parse_variations_response(raw: str, competitors: list) -> dict[str, list[str]]:
    """Parse the LLM response for competitor variations into a name -> variations map."""
    # Build a lowercase lookup for case-insensitive matching
    lower_to_canonical = {comp.lower(): comp for comp in competitors}
    variations_map: dict[str, list[str]] = {}

    for line in raw.strip().split("\n"):
        if ":" not in line:
            continue
        name, _, variations_str = line.partition(":")
        canonical = lower_to_canonical.get(name.strip().lower())
        if canonical is None:
            continue
        variations = [
            v.strip()
            for v in variations_str.split(",")
            if v.strip() and v.strip().lower() != canonical.lower()
        ]
        variations_map[canonical] = variations

    return variations_map

