from typing import Any

def get_scaling_options(
    mat_a: Any,
    mat_b: Any,
    scale_a_size: torch.Tensor,
    scale_b_size: torch.Tensor,
) -> tuple[ScalingType, ScalingType]:
    for scale_option_a, scale_option_b in scaling_pairs:
        if is_desired_scaling(
            mat_a, scale_a_size, scale_option_a
        ) and is_desired_scaling(mat_b, scale_b_size, scale_option_b, transpose=True):
            return scale_option_a, scale_option_b

    raise AssertionError(
        f"Inductor Triton does not support scale_a.shape = {scale_a_size}, scale_b.shape = {scale_b_size}"
    )  # verify that shapes are supported by at least one existing pairing

