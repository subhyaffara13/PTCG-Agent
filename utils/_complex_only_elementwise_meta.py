
def _complex_only_elementwise_meta(*args, **kwargs):
    torch._check(
        utils.is_complex_dtype(args[0].dtype), lambda: "Only complex dtype is supported"
    )
    return _prim_elementwise_meta(*args, **kwargs)

