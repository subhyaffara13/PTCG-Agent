
def _get_input_paths(example_inputs, signature):
    """
    Generate paths of placeholders, needed for generating the guards function.

    NOTE: Here we make use of the example inputs used for export as well as
    the signature of the unlifted graph module (not preserved by export).
    """

    args, kwargs = example_inputs
    binded = signature.bind(*args, **kwargs)
    binded.apply_defaults()
    ctx = binded.arguments
    flat_example_inputs_with_paths = pytree.tree_leaves_with_path(ctx)
    return [path for path, _ in flat_example_inputs_with_paths]

