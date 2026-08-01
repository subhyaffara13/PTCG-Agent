
def random_sparse_matrix(rows, columns, density=0.01, **kwargs):
    """Return rectangular random sparse matrix within given density.

    The density of the result approaches to given density as the size
    of the matrix is increased and a relatively small value of density
    is specified but higher than min(rows, columns)/(rows * columns)
    for non-singular matrices.
    """
    dtype = kwargs.get('dtype', torch.double)
    device = kwargs.get('device', 'cpu')

    nonzero_elements = max(min(rows, columns), int(rows * columns * density))
    indices = _generate_indices_prefer_all_rows(rows, columns, nonzero_elements)
    values = torch.randn(nonzero_elements, dtype=dtype, device=device)

    # ensure that the diagonal dominates
    values *= torch.tensor([-float(i - j)**2 for i, j in indices], dtype=dtype, device=device).exp()
    A = torch.sparse_coo_tensor(indices.t(), values, (rows, columns), device=device)
    return A.coalesce()

