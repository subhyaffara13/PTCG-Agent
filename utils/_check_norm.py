
def _check_norm(elements, norm):
    """validate if input norm is consistent"""
    if norm is not None and norm.is_number:
        if norm.is_positive is False:
            raise ValueError("Input norm must be positive.")

        numerical = all(i.is_number and i.is_real is True for i in elements)
        if numerical and is_eq(norm**2, sum(i**2 for i in elements)) is False:
            raise ValueError("Incompatible value for norm.")

