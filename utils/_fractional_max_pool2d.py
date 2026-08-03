from typing import Optional

def _fractional_max_pool2d(
    input: Tensor,
    kernel_size: BroadcastingList2[int],
    output_size: Optional[BroadcastingList2[int]] = None,  # noqa: UP045
    output_ratio: Optional[BroadcastingList2[float]] = None,  # noqa: UP045
    return_indices: bool = False,
    _random_samples: Tensor | None = None,
) -> Tensor:
    if has_torch_function_variadic(input, _random_samples):
        return handle_torch_function(
            fractional_max_pool2d,
            (input, _random_samples),
            input,
            kernel_size,
            output_size=output_size,
            output_ratio=output_ratio,
            return_indices=return_indices,
            _random_samples=_random_samples,
        )
    return fractional_max_pool2d_with_indices(
        input, kernel_size, output_size, output_ratio, return_indices, _random_samples
    )[0]

