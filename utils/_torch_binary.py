
def _torch_binary(fn_name):
    fn = getattr(torch.ops.aten, fn_name)

    def binary_fn(*args, **kwargs):
        return _binary_helper(fn, args, kwargs, inplace=False)

    return binary_fn

