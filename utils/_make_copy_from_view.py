
def _make_copy_from_view(fn, return_none_on_out_variant=False):
    """
    Given a view function (e.g. torch.diagonal) generates its copy variant (e.g. torch.diagonal_copy)
    """
    aten_fn = getattr(aten, fn.__name__)
    annotations = getattr(fn, "__annotations__", {})
    # view ops should not change dtypes, this ensures that the decomp path has
    # the same error checks as eager.
    fn = out_wrapper(exact_dtype=True)(aten_fn)

    @wraps(fn)
    def _fn(*args, out=None, **kwargs):
        result = fn(*args, out=out, **kwargs)
        if return_none_on_out_variant and out is not None:
            return None
        if out is not None:
            return result

        return pytree.tree_map(
            lambda x: x.clone(memory_format=torch.contiguous_format),
            result,
        )

    copy_name = f"{fn.__name__}_copy"
    _fn.__name__ = copy_name
    _fn.__annotations__.update(annotations)
    register_decomposition(getattr(aten, copy_name))(_fn)
    return _fn

