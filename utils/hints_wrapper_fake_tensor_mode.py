
def hints_wrapper_fake_tensor_mode(mode, body_func, args, kwargs, hints):
    flat_args = pytree.tree_leaves(args)
    with mode:
        return body_func(*flat_args, **kwargs)

