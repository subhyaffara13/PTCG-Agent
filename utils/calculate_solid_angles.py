
def calculate_solid_angles(R):
    """Calculates the solid angles of plane triangles. Implements the method of
    Van Oosterom and Strackee [VanOosterom]_ with some modifications. Assumes
    that input points have unit norm."""
    # Original method uses a triple product `R1 . (R2 x R3)` for the numerator.
    # This is equal to the determinant of the matrix [R1 R2 R3], which can be
    # computed with better stability.
    numerator = np.linalg.det(R)
    denominator = 1 + (np.einsum('ij,ij->i', R[:, 0], R[:, 1]) +
                       np.einsum('ij,ij->i', R[:, 1], R[:, 2]) +
                       np.einsum('ij,ij->i', R[:, 2], R[:, 0]))
    return np.abs(2 * np.arctan2(numerator, denominator))

