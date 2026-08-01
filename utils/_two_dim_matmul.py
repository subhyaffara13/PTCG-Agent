
def _two_dim_matmul(x, matrix_dim_one, matrix_dim_two):
    """Applies 2D matrix multiplication to 3D input arrays."""
    seq_length = x.shape[1]
    matrix_dim_one = matrix_dim_one[:seq_length, :seq_length]
    x = x.type(torch.complex64)
    return torch.einsum("bij,jk,ni->bnk", x, matrix_dim_two, matrix_dim_one)

