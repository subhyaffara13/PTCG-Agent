
def index_variable(shape, max_indices, device=torch.device('cpu')):
    if not isinstance(shape, tuple):
        shape = (shape,)
    return torch.testing.make_tensor(*shape, dtype=torch.long, device=device, low=0, high=max_indices)

