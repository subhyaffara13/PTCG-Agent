
def get_opinfo_by_name(name: str) -> list[opinfo_core.OpInfo]:
    """Find OpInfo entries by exact operator name."""
    matches = [op for op in op_db if op.name == name]
    if matches:
        return matches

    # Suggest alternatives
    candidates = _find_opinfo_candidates(name)
    if candidates:
        suggestions = ", ".join(f'"{c}"' for c in candidates)
        raise ValueError(f'No OpInfo found for "{name}", did you mean: {suggestions}?')
    raise ValueError(
        f'No OpInfo found for "{name}". OpInfo is required as it provides '
        f"sample inputs for the operator."
    )

