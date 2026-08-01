
def is_nonfreeable_buffers(dep: Dep) -> bool:
    from .virtualized import V

    dep_name = dep.name
    # Subgraphs have a prefix for the name, cleanup the prefix
    # before checking for known strings.
    if V.graph.name:
        dep_name = dep_name.removeprefix(V.graph.name + "_")
    return dep_name.startswith(
        ("primals_", "arg", "fwd_rng_state", "bwd_rng_state", "tangents")
    )

