
def _check_inputs_match(args, kwargs, in_spec: pytree.TreeSpec) -> list:
    reordered_kwargs = reorder_kwargs(kwargs, in_spec)
    flat_args_with_path, received_spec = pytree.tree_flatten_with_path(
        (args, reordered_kwargs)
    )

    if not eq_spec(received_spec, in_spec):
        raise ValueError(  # noqa: B904
            "Trying to flatten user inputs with exported input tree spec: \n"
            f"{in_spec}\n"
            "but actually got inputs with tree spec of: \n"
            f"{received_spec}.\n"
            "Please check that the inputs have the same number and type of "
            "args and kwargs as the ones you used when tracing."
        )

    return flat_args_with_path

