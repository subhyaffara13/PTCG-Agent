
def _remove_nulls(x: Dict[str, Any]) -> Dict[str, Any]:
    """Remove None values from dict."""
    return {k: v for k, v in x.items() if v is not None}

