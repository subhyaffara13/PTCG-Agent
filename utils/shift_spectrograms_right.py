
def shift_spectrograms_right(
    input_values: torch.Tensor, reduction_factor: int = 1, attention_mask: torch.Tensor | None = None
):
    """
    Shift input spectrograms one timestep to the right. Also applies the reduction factor to the sequence length.
    """
    # thin out frames for reduction factor
    if reduction_factor > 1:
        input_values = input_values[:, reduction_factor - 1 :: reduction_factor]
        if attention_mask is not None:
            attention_mask = attention_mask[:, reduction_factor - 1 :: reduction_factor]

    shifted_input_values = input_values.new_zeros(input_values.shape)
    shifted_input_values[:, 1:] = input_values[:, :-1].clone()

    # replace possible -100 values in labels by zeros
    shifted_input_values.masked_fill_(shifted_input_values == -100.0, 0.0)

    return shifted_input_values, attention_mask

