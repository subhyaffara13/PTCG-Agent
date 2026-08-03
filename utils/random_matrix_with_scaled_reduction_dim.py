import math


def random_matrix_with_scaled_reduction_dim(rows, columns, *batch_dims, **kwargs):
    """Return rectangular matrix or batches of rectangular matrices
    with entries being iid and sampled from N(0, sigma^2) such that
    the variance of (A @ A.T)[..., i, j] is 1 if reduction_dim=-1, or
    the variance of (A.T @ A)[..., i, j] is 1 if reduction_dim=-2.

    Parameters:
      dtype - the data type
      device - the device kind
      requires_grad - whether output requires grad
      reduction_dim - the row/column dimension to re-scale.
                    Expected to be either -1 (columns) or -2 (rows).
    """
    dtype = kwargs.get('dtype', torch.double)
    device = kwargs.get('device', 'cpu')
    requires_grad = kwargs.get('requires_grad', False)
    reduction_dim = kwargs.get('reduction_dim', -1)

    shape = (*batch_dims, rows, columns)
    red_scale = math.sqrt(shape[reduction_dim])
    res = torch.randn(*shape, dtype=dtype, device=device) / red_scale
    res.requires_grad_(requires_grad)
    return res

