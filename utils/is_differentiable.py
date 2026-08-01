
def is_differentiable(
    name: str, type: Type, info: DifferentiabilityInfo | None
) -> bool:
    return type.is_tensor_like() and (
        info is None or name not in info.non_differentiable_arg_names
    )

