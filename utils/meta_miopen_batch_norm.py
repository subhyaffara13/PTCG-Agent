
def meta_miopen_batch_norm(
    input_tensor: torch.Tensor,
    weight: torch.Tensor,
    bias: torch.Tensor | None,
    running_mean: torch.Tensor | None,
    running_var: torch.Tensor | None,
    training: bool,
    exponential_average_factor: float,
    epsilon: float,
):
    # In batch norm the output is of the same shape as the input
    out_shape = input_tensor.shape

    # If tensor is provided for running_mean and running_var then use this. If these are not
    # provided then we return the shape of weight tensor. Similar to how this is handled in the decomposition
    save_mean_shape = running_mean.shape if running_mean is not None else weight.shape
    save_var_shape = running_var.shape if running_var is not None else weight.shape

    def pick_memory_format():
        if is_channels_last(input_tensor):
            return torch.channels_last
        if input_tensor.is_contiguous(memory_format=torch.contiguous_format):
            return torch.contiguous_format
        return torch.contiguous_format

    out = input_tensor.new_empty(out_shape).to(memory_format=pick_memory_format())

    if training:
        save_mean = input_tensor.new_empty(save_mean_shape)
        save_var = input_tensor.new_empty(save_var_shape)
    else:
        save_mean = input_tensor.new_empty((0,))
        save_var = input_tensor.new_empty((0,))

    return out, save_mean, save_var

