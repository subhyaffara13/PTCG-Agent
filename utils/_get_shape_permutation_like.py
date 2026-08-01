
def _get_shape_permutation_like(
    self: torch.Tensor,
) -> tuple[utils.ShapeType, utils.StrideType]:
    physical_layout, _ = utils.compute_elementwise_output_logical_to_physical_perm(self)
    shape = [self.shape[l] for l in physical_layout]

    permutation = [0] * len(shape)
    for p, l in enumerate(physical_layout):
        permutation[l] = p

    return (shape, permutation)

