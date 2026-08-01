
def count_tangents(fx_g: torch.fx.GraphModule) -> int:
    """
    Infers which inputs are static for a backwards graph
    """

    def is_saved_tensor(x: Node) -> bool:
        return (
            "tangents" not in x.name
            and "bwd_seed" not in x.name
            and "bwd_base_offset" not in x.name
            and "bwd_rng_state" not in x.name
        )

    arg_count = 0
    static_arg_idxs = []
    for n in fx_g.graph.nodes:
        if n.op == "placeholder":
            if is_saved_tensor(n):
                static_arg_idxs.append(arg_count)
            arg_count += 1

    assert static_arg_idxs == list(range(len(static_arg_idxs)))
    return len(static_arg_idxs)

