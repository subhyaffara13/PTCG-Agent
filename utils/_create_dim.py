
def _create_dim(name: str, size: int | None = None) -> Dim:
    """Create a new Dim object."""
    return Dim(name, size if size is not None else -1)

