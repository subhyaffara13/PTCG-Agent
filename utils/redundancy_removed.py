
def redundancy_removed(A, B):
    """Checks whether a matrix contains only independent rows of another"""
    for rowA in A:
        # `rowA in B` is not a reliable check
        for rowB in B:
            if np.all(rowA == rowB):
                break
        else:
            return False
    return A.shape[0] == np.linalg.matrix_rank(A) == np.linalg.matrix_rank(B)

