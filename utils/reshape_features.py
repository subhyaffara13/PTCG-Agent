
def reshape_features(hidden_states: torch.Tensor) -> torch.Tensor:
    """Discard class token and reshape 1D feature map to a 2D grid."""
    n_samples, seq_len, hidden_size = hidden_states.shape
    size = torch_int(seq_len**0.5)

    hidden_states = hidden_states[:, -(size**2) :, :]  # remove special tokens if there are any
    hidden_states = hidden_states.reshape(n_samples, size, size, hidden_size)
    hidden_states = hidden_states.permute(0, 3, 1, 2)

    return hidden_states

