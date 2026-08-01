
def keep_portable_guards_unsafe(guard_entries):
    """
    A common function to only keep guards that can be used in both Python and non-Python environments.
    This includes:
    - Tensor metadata and dynamic shape information.
    - Global contexts state (e.g. autocast, no_grad, etc.)

    This is unsafe to use by default.
    To use this API, use guard_filter_fn argument while calling torch.compile

    >> opt_mod = torch.compile(
    >>     mod,
    >>     options={"guard_filter_fn": torch.compiler.keep_global_context_and_tensor_guards_unsafe},
    >> )
    """
    return [
        (
            g.guard_type in ("GLOBAL_STATE", "SHAPE_ENV")
            or (g.guard_type == "TENSOR_MATCH" and not g.is_global)
        )
        for g in guard_entries
    ]

