
def is_coalesced_indices(s):
    indices = s._indices()
    hash_coeffs = (1,) + s.shape[s.sparse_dim() - 1:0:-1]
    hash_indices = torch.tensor(hash_coeffs, device=s.device).cumprod(-1).flip(-1)
    if s.sparse_dim() > 1:
        hash_indices.unsqueeze_(-1)
        hash_indices = (indices * hash_indices).sum(0)
    else:
        hash_indices = indices * hash_indices

    # check if indices are sorted
    res = torch.allclose(hash_indices, hash_indices.sort()[0])

    # check if there are no repeated indices
    res = res and torch.allclose(hash_indices, hash_indices.unique())

    return res

