
def get_group_name(n: fx.Node) -> str:
    """Extract the group name from a collective operation node."""
    opt_args_kwargs = normalize_function(
        n.target,  # type: ignore[arg-type]
        args=n.args,
        kwargs=n.kwargs,
        normalize_to_only_use_kwargs=True,
    )
    assert opt_args_kwargs is not None
    _, kwargs = opt_args_kwargs
    return kwargs["group_name"]

