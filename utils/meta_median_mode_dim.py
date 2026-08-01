
def meta_median_mode_dim(input, dim=-1, keepdim=False):
    if device_hint(input) == "cuda":
        utils.alert_not_deterministic("median CUDA with indices output")
    dim = utils.reduction_dims(input.shape, (dim,))
    output_shape = _compute_reduction_shape(input, dim, keepdim)
    return (
        input.new_empty(output_shape),
        input.new_empty(output_shape, dtype=torch.long),
    )

