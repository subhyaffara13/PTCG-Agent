
def _is_tensor_within_2gb(arg: TensorArg) -> bool:
    """Check if a tensor argument's storage is provably within 2GB.

    Mirrors HIPBackend.is_within_2gb() but uses compile-time symbolic analysis
    instead of runtime tensor inspection. This enables canonicalize_pointers to
    decompose pointer arithmetic into (splat(base), offset) form for buffer ops.
    """
    MAX_BYTES = 2**31 - 1
    try:
        # Graph inputs aren't tracked by the scheduler; get their layout
        # from the graph_inputs dict to avoid KeyError in get_buffer_layout.
        if arg.buffer in V.graph.graph_inputs:
            inp = V.graph.graph_inputs[arg.buffer]
            if hasattr(inp, "get_layout"):
                layout = inp.get_layout()
            else:
                return False
        else:
            layout = _get_buffer_layout(arg.buffer)
        storage_bytes = layout.storage_size() * arg.dtype.itemsize
        return V.graph.sizevars.statically_known_true(storage_bytes <= MAX_BYTES)
    except Exception:
        return False

