
def is_tensor_partial(spec: DTensorSpec) -> bool:
    """Return True if tensor is partial on the mesh."""
    return any(p.is_partial() for p in spec.placements)

