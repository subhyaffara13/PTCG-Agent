
def _load_finegrained_fp8_kernel() -> FineGrainedFP8:
    """
    Load the finegrained-fp8 Triton kernel once and return its entry points.

    Raises `ImportError` if the `kernels` package is missing, or the kernel or required
    symbols cannot be found.
    """
    if not is_torchdynamo_compiling():
        if not is_kernels_available():
            raise ImportError(
                "finegrained-fp8 kernel requires the `kernels` package. Install it with `pip install -U kernels`."
            )

    kernel = lazy_load_kernel("finegrained-fp8")
    if kernel is None:
        raise ImportError(
            "Failed to load the finegrained-fp8 kernel — check that `kernels-community/finegrained-fp8` "
            "has a build matching the current torch/CUDA."
        )

    matmul = getattr(kernel, "matmul", None)
    batched_matmul = getattr(kernel, "matmul_batched", None)
    grouped_matmul = getattr(kernel, "matmul_grouped", None)

    missing = [
        name
        for name, attr in [
            ("matmul", matmul),
            ("matmul_batched", batched_matmul),
            ("matmul_grouped", grouped_matmul),
        ]
        if attr is None
    ]
    if missing:
        raise ImportError(
            f"finegrained-fp8 kernel is missing required symbols: {', '.join(missing)}. "
            "Please update the `kernels` package (`pip install -U kernels`)."
        )

    return FineGrainedFP8(
        matmul=matmul,
        batched_matmul=batched_matmul,
        grouped_matmul=grouped_matmul,
    )

