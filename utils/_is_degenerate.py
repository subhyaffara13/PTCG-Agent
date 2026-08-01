
def _is_degenerate(system: list[Poly]) -> bool:
    """Helper function to check if a system is degenerate"""
    return any(p.is_ground for p in system)

