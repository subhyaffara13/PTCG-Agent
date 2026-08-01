
def register_barrier(barrier_class: type) -> type:
    """Register a barrier class in the global registry."""
    if hasattr(barrier_class, "barrier_type"):
        BARRIER_REGISTRY[barrier_class.barrier_type] = barrier_class
    return barrier_class

