
def keep_tensor_guards_unsafe(guard_entries, keep_parameters=False):
    """
    A common function to keep tensor guards on all tensors. This is unsafe to
    use by default. But if you don't expect any changes in the model code, you
    can just keep the tensor guards.


    >> opt_mod = torch.compile(
    >>     mod,
    >>     options={"guard_filter_fn": torch.compiler.keep_tensor_guards},
    >> )
    """

    keep_flags = []
    for entry in guard_entries:
        if entry.guard_type == "TENSOR_MATCH":
            if not isinstance(entry.value, torch.nn.Parameter):
                keep_flags.append(True)
            elif keep_parameters:
                keep_flags.append(True)
            else:
                keep_flags.append(False)
        else:
            keep_flags.append(False)
    return keep_flags

