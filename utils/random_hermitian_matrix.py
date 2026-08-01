
def random_hermitian_matrix(l, *batches, **kwargs):
    dtype = kwargs.get('dtype', torch.double)
    device = kwargs.get('device', 'cpu')
    A = torch.randn(*(batches + (l, l)), dtype=dtype, device=device)
    A = (A + A.mH).div_(2)
    return A

