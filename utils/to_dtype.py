
def to_dtype(
    x: TensorBox, dtype: torch.dtype, copy: bool = False, use_compute_types: bool = True
):
    src_dtype = x.get_dtype()
    if src_dtype == dtype:
        return clone(x) if copy else x

    def _to_dtype(x):
        result = ops.to_dtype(
            x,
            dtype,
            src_dtype=src_dtype,
            use_compute_types=use_compute_types,
        )
        low_pr_fp = (torch.bfloat16, torch.float16)
        if not use_compute_types and dtype in low_pr_fp:
            # Upcast back to compute type so fused consumers see a compute-type
            # value. Without this, a raw low-precision value gets a redundant
            # downcast from the consumer's input emulation.
            result = ops.to_dtype(result, dtype)
        return result

    return make_pointwise(_to_dtype, override_return_dtype=dtype)(x)


def to_dtype(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")

    return NestedTensor(func(inp._values, **new_kwargs), **extract_kwargs(inp))

