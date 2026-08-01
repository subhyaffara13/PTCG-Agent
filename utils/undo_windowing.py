
def undo_windowing(hidden_states: torch.Tensor, shape: list[int], mask_unit_shape: list[int]) -> torch.Tensor:
    """
    Restore spatial organization by undoing windowed organization of mask units.

    Args:
        hidden_states (`torch.Tensor`): The hidden states tensor of shape `[batch_size, num_mask_unit_height*num_mask_unit_width, hidden_size]`.
        shape (`list[int]`): The original shape of the hidden states tensor before windowing.
        mask_unit_shape (`list[int]`): The shape of the mask units used for windowing.

    Returns:
        torch.Tensor: The restored hidden states tensor of shape [batch_size, num_mask_unit_height*mask_unit_height, num_mask_unit_width*mask_unit_width, hidden_size].
    """
    batch_size, hidden_size = hidden_states.shape[0], hidden_states.shape[-1]
    # From: [batch_size, num_mask_unit_height*num_mask_unit_width, hidden_size]
    # To: [batch_size, num_mask_unit_height, num_mask_unit_width, mask_unit_height, mask_unit_width, hidden_size]
    num_mask_units = [s // mu for s, mu in zip(shape, mask_unit_shape)]
    hidden_states = hidden_states.view(batch_size, *num_mask_units, *mask_unit_shape, hidden_size)

    # From: [batch_size, num_mask_unit_height, num_mask_unit_width, mask_unit_height, mask_unit_width, hidden_size]
    # To: [batch_size, num_mask_unit_height*mask_unit_height, num_mask_unit_width*mask_unit_width, hidden_size]
    hidden_states = hidden_states.permute(0, 1, 3, 2, 4, 5)
    hidden_states = hidden_states.reshape(batch_size, *shape, hidden_size)

    return hidden_states

