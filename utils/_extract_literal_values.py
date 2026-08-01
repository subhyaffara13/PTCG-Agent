
def _extract_literal_values(annotation: Any) -> List[str]:
    """
    Extract literal values from a Literal type annotation
    """
    if hasattr(annotation, "__origin__") and hasattr(annotation, "__args__"):
        origin = annotation.__origin__
        if hasattr(origin, "__name__") and origin.__name__ == "Literal":
            return list(annotation.__args__)
    return []

