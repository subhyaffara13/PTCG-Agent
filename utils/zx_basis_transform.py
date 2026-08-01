
def zx_basis_transform(self, format='sympy'):
    """Transformation matrix from Z to X basis."""
    return matrix_cache.get_matrix('ZX', format)

