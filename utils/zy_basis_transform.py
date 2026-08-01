
def zy_basis_transform(self, format='sympy'):
    """Transformation matrix from Z to Y basis."""
    return matrix_cache.get_matrix('ZY', format)

