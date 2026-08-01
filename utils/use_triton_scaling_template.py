
def use_triton_scaling_template(
    scale_option_a: ScalingType,
    scale_option_b: ScalingType,
    scaling_types: list[ScalingType],
) -> bool:
    return scale_option_a in scaling_types and scale_option_b in scaling_types

