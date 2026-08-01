
def make_reduction(reduction_type: ReductionType, override_return_dtype=None):
    def inner(x, axis=None, keepdims=False, *, dtype=None):
        # For argmax/argmin on boolean tensors, cast to int32 first to ensure
        # correct comparison in Triton. See https://github.com/pytorch/pytorch/issues/174069
        # Only apply on Triton backend; MPS handles bool comparisons natively.
        if (
            reduction_type in ("argmax", "argmin")
            and x.get_dtype() == torch.bool
            and is_triton(x)
        ):
            x = to_dtype(x, torch.int32)
        kwargs = _make_reduction_inner(
            x,
            axis=axis,
            keepdims=keepdims,
            dtype=dtype,
            override_return_dtype=override_return_dtype,
            reduction_type=reduction_type,
        )
        result = Reduction.create(reduction_type=reduction_type, input_node=x, **kwargs)
        if isinstance(
            result.data.data,  # type: ignore[attr-defined, attr-type, union-attr]
            Reduction,
        ):  # Only realize if reduction isn't unrolled
            result.realize()
        return result

    return inner

