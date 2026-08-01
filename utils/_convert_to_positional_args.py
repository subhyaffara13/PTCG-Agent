
def _convert_to_positional_args(orig_arg_names, args, kwargs):
    if len(orig_arg_names) != len(args) + len(kwargs):
        raise AssertionError(
            f"Total number of arg names is expected to be {len(orig_arg_names)} "
            f"but got {len(args)} positional args, {len(kwargs)} kwargs."
        )
    reordered_kwargs = [kwargs[kw_name] for kw_name in orig_arg_names[len(args) :]]
    return (
        *args,
        *reordered_kwargs,
    )

