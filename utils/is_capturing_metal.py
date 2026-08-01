
def is_capturing_metal() -> bool:
    """Checks if metal capture is in progress"""
    return torch._C._mps_isCapturing()  # type: ignore[attr-defined, no-any-return]

