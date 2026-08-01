
def _format_not_finite(value: float) -> str:
    """Utility function to handle infinite and nan cases."""
    import math

    if math.isnan(value):
        return "NaN"
    if math.isinf(value) and value < 0:
        return "-Inf"
    if math.isinf(value) and value > 0:
        return "+Inf"
    return ""

