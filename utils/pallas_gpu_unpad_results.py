
def pallas_gpu_unpad_results(
    results: Any,
    orig_shapes: tuple[Any, ...],
    is_scalar_output: list[bool] | None = None,
) -> Any:
    """Remove padding from GPU kernel results and reshape to original shapes.

    If is_scalar_output is None, all outputs are treated as non-scalar.
    """
    if not isinstance(results, tuple):
        results = (results,)
    unpadded = []
    for i, (res, shape) in enumerate(zip(results, orig_shapes)):
        if is_scalar_output is not None and is_scalar_output[i]:
            unpadded.append(res)
        else:
            orig_numel = math.prod(shape)
            unpadded.append(res[:orig_numel].reshape(shape))
    return unpadded[0] if len(unpadded) == 1 else tuple(unpadded)

