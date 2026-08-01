
def _foreach_lerp_scalar(
    start_tensors: list[torch.Tensor],
    end_tensors: list[torch.Tensor],
    weight: torch.types.Number,
) -> list[torch.Tensor]:
    return aten._foreach_add.List(
        start_tensors,
        aten._foreach_mul.Scalar(
            aten._foreach_sub.List(end_tensors, start_tensors), weight
        ),
    )

