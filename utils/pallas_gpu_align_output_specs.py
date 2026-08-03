from typing import Any
import math


def pallas_gpu_align_output_specs(
    out_shapes: tuple[Any, ...],
    out_dtypes: tuple[Any, ...],
    alignment: int = 128,
) -> tuple[tuple[Any, ...], list[bool]]:
    """Build aligned output ShapeDtypeStruct specs for GPU kernels.

    Returns (aligned_specs, is_scalar_output) where is_scalar_output[i] is True
    when the i-th output is scalar and should not be padded/unpadded.
    """
    import jax  # pyrefly: ignore [import-error, missing-import]

    aligned_specs = []
    is_scalar = []
    for shape, dtype in zip(out_shapes, out_dtypes):
        numel = math.prod(shape)
        if numel <= 1:
            aligned_specs.append(jax.ShapeDtypeStruct(shape, dtype))
            is_scalar.append(True)
        else:
            aligned_numel = ((numel + alignment - 1) // alignment) * alignment
            aligned_specs.append(jax.ShapeDtypeStruct((aligned_numel,), dtype))
            is_scalar.append(False)
    return tuple(aligned_specs), is_scalar

