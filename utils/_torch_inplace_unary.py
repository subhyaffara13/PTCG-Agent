
def _torch_inplace_unary(fn_name):
    fn = getattr(torch.ops.aten, fn_name)

    def unary_fn(*args, **kwargs):
        return _unary_helper(fn, args, kwargs, inplace=True)

    return unary_fn

