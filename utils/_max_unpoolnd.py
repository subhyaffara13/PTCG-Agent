
def _max_unpoolnd(
    self: TensorLike, indices: TensorLike, output_size: list[int], dim: int
):
    # If the input tensors self and indices came from max_pool call as
    # required by the documentation, this operation is deterministic
    # because that ensures that if there are two entries in `indices`
    # tensor that are equal, the corresponding values in `self` are also
    # equal. If this condition is not satisfied, the operation is
    # non-deterministic as one of the different values in `self` 'wins'.
    utils.alert_not_deterministic(f"max_unpooling{dim}d_forward_out")
    output_shape = list(self.shape[:-dim]) + list(output_size)
    if any(s == 0 for s in output_shape):
        return self.new_zeros(output_shape)
    nc = reduce(operator.mul, self.shape[:-dim])
    hw = reduce(operator.mul, output_size)
    indices_nc_shape = [1] * self.ndim
    indices_nc_shape[:-dim] = self.shape[:-dim]
    indices_flat = (
        indices + aten.arange(nc, device=self.device).view(indices_nc_shape) * hw
    ).reshape(-1)

    output = self.new_zeros(output_shape)
    return aten._unsafe_index_put(
        output.reshape(-1), [indices_flat], self.reshape(-1), accumulate=False
    ).view(output.shape)

