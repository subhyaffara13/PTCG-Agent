
def estimate_fx_collective_size(fx_node: torch.fx.Node) -> int:
    """Estimate the size of a collective operation in bytes, including inputs and outputs."""
    input_bytes = None

    args, kwargs = fx_node.args, fx_node.kwargs
    kwargs = dict(kwargs)

    # dont double count pre-allocated buffer passed in
    kwargs.pop("out", None)

    def tensor_bytes(t: torch.Tensor) -> int:
        return get_fx_node_size_numel(t.size()) * get_dtype_size(t.dtype)

    def add_inp_bytes(inp: torch.fx.Node):
        inp_val = inp.meta.get("val", None)
        if not isinstance(inp_val, torch.Tensor):
            return

        nonlocal input_bytes
        if input_bytes is None:
            input_bytes = 0
        input_bytes += tensor_bytes(inp_val)

    pytree.tree_map_only(
        torch.fx.Node,
        add_inp_bytes,
        (args, kwargs),
    )

    output_val = fx_node.meta.get("val", None)

    if input_bytes is None or output_val is None:
        return 0

    # Coalesced collectives return a list of tensors
    if isinstance(output_val, (list, tuple)):
        output_bytes = sum(
            tensor_bytes(t) for t in output_val if isinstance(t, torch.Tensor)
        )
    elif isinstance(output_val, torch.Tensor):
        output_bytes = tensor_bytes(output_val)
    else:
        return 0

    return input_bytes + output_bytes

