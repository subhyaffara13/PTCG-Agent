
def gather_variable(shape, index_dim, max_indices, duplicate=False, device=torch.device('cpu')):
    if len(shape) != 2:
        raise AssertionError(f"Expected len(shape) == 2, got {len(shape)}")
    if index_dim >= 2:
        raise AssertionError(f"Expected index_dim < 2, got {index_dim}")
    batch_dim = 1 - index_dim
    index = torch.zeros(*shape, dtype=torch.long, device=device)
    for i in range(shape[index_dim]):
        index.select(index_dim, i).copy_(
            torch.randperm(max_indices, device=device)[:shape[batch_dim]])
    if duplicate:
        index.select(batch_dim, 0).copy_(index.select(batch_dim, 1))
    return index

