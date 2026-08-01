
def random_symmetric_pd_matrix(matrix_size, *batch_dims, **kwargs):
    dtype = kwargs.get('dtype', torch.double)
    device = kwargs.get('device', 'cpu')
    A = torch.randn(*(batch_dims + (matrix_size, matrix_size)),
                    dtype=dtype, device=device)
    return torch.matmul(A, A.mT) \
        + torch.eye(matrix_size, dtype=dtype, device=device) * 1e-5

