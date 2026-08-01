
def _get_or_create_library(op_symbol: str, dispatch_key: str) -> torch.library.Library:
    """
    Get or create a torch.library.Library instance for the given key.

    Args:
        op_symbol: The operation symbol
        dispatch_key: The dispatch key

    Returns:
        torch.library.Library: The library instance
    """
    global _libs

    key = (op_symbol, dispatch_key)
    if key not in _libs:
        _libs[key] = torch.library.Library("aten", "IMPL", dispatch_key)

    return _libs[key]

