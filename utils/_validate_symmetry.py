
def _validate_symmetry(symmetry):
    """
    Check that the symmetry parameter is one that MatrixMarket allows..
    """
    if symmetry is None:
        return "general"

    symmetry = str(symmetry).lower()
    symmetries = ["general", "symmetric", "skew-symmetric", "hermitian"]
    if symmetry not in symmetries:
        raise ValueError("Invalid symmetry. Must be one of: " + ", ".join(symmetries))

    return symmetry

