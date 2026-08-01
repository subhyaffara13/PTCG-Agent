
def control_deps_eager(additional_deps, subgraph, *args, **kwargs):
    """Eager implementation - just execute the subgraph."""
    return subgraph(*args, **kwargs)

