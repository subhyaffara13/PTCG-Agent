
def reference_masked_std_var(
    numpy_fn,
):
    ref = reference_reduction_numpy(numpy_fn)

    # Translate unbiased or correction arguments into ddof
    def func(
        input,
        dim=None,
        unbiased=None,
        *,
        correction=None,
        **kwargs,
    ):
        ddof = 1
        if unbiased is not None:
            ddof = 1 if unbiased else 0
        if correction is not None:
            ddof = correction

        if isinstance(dim, Sequence):
            dim = tuple(dim)

        return ref(input, dim, ddof=ddof, **kwargs)

    return func

