
def reshape_for_broadcast(freqs_ci: torch.Tensor, query: torch.Tensor):
    ndim = query.ndim
    shape = [d if i == 1 or i == ndim - 1 else 1 for i, d in enumerate(query.shape)]
    return freqs_ci.view(*shape)

