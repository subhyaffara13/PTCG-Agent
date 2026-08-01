
def _normalized_like(A, B):
    return A * (scipy.linalg.norm(B) / scipy.linalg.norm(A))

