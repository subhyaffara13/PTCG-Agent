
def _flatten_inputs(model_args, model_kwargs):
    flattened_args, _ = _pytree.tree_flatten((model_args, model_kwargs))
    return flattened_args

