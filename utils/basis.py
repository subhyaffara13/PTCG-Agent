
def basis(A):
    """Return orthogonal basis of A columns."""
    return torch.linalg.qr(A).Q

