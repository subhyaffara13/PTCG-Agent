
def sum_to_size(
    a: Tensor,
    *shape,
) -> Tensor:
    shape = utils.extract_shape_from_varargs(shape, validate=False)
    torch._check(
        utils.is_expandable_to(shape, a.shape),
        lambda: f'sum_to_size: size "{shape}" is not expandable to size "{a.shape}"',
    )
    # In ATen scalar tensors are sent through sum and the result is returned as
    # type promoted
    if utils.is_same_shape(shape, a.shape) and len(shape) > 0:
        return prims.view_of(a)
    leading_dims = a.ndim - len(shape)
    reduce_dims = tuple(range(leading_dims)) + tuple(
        i
        for i in range(leading_dims, len(shape))
        if shape[i - leading_dims] == 1 and a.shape[i] != 1
    )
    return torch.sum(a, dim=reduce_dims, keepdim=True, dtype=None)

