
def _simplify_matrix(M):
    """Return a simplified copy of the matrix M"""
    if not isinstance(M, (Matrix, ImmutableMatrix)):
        raise TypeError("The matrix M must be an instance of Matrix or ImmutableMatrix")
    Mnew = M.as_mutable() # makes a copy if mutable
    Mnew.simplify()
    if isinstance(M, ImmutableMatrix):
        Mnew = Mnew.as_immutable()
    return Mnew

