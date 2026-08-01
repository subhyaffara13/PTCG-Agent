
def flatten_final_dims(t: torch.Tensor, no_dims: int):
    return t.reshape(t.shape[:-no_dims] + (-1,))


def flatten_final_dims(t: torch.Tensor, no_dims: int) -> torch.Tensor:
    return t.reshape(t.shape[:-no_dims] + (-1,))

