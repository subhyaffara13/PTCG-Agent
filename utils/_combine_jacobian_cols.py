
def _combine_jacobian_cols(
    jacobians_cols: dict[int, list[torch.Tensor]], outputs, input, numel
) -> tuple[torch.Tensor, ...]:
    # jacobian_cols maps column_idx -> output_idx -> single column of jacobian Tensor
    # we return a list that maps output_idx -> full jacobian Tensor
    jacobians = _allocate_jacobians_with_outputs(
        outputs, numel, dtype=input.dtype if input.dtype.is_complex else None
    )
    for i, jacobian in enumerate(jacobians):
        for k, v in jacobians_cols.items():
            jacobian[k] = v[i]
    return jacobians

