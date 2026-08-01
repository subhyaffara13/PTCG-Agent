
def _format_boolop(explanations: Iterable[str], is_or: bool) -> str:
    explanation = "(" + ((is_or and " or ") or " and ").join(explanations) + ")"
    return explanation.replace("%", "%%")

