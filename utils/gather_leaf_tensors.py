
def gather_leaf_tensors(args, kwargs):
    leaf_tensors = []
    args, _args_spec = tree_flatten(args)
    kwargs, _kwargs_spec = tree_flatten(kwargs)
    args = args + kwargs
    for arg in args:
        if not isinstance(arg, torch.Tensor):
            continue
        if arg.requires_grad:
            leaf_tensors.append(arg)
    return leaf_tensors

