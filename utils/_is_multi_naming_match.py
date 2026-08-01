
def _is_multi_naming_match(
    match: re.Match[str] | None, node_type: str, confidence: interfaces.Confidence
) -> bool:
    return (
        match is not None
        and match.lastgroup is not None
        and match.lastgroup not in EXEMPT_NAME_CATEGORIES
        and not (node_type == "method" and confidence == interfaces.INFERENCE_FAILURE)
    )

