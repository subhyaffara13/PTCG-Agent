
def sparse_may_share_memory(A, B):
    # Checks if A and B have any numpy array sharing memory.

    def _underlying_arrays(x):
        # Given any object (e.g. a sparse array), returns all numpy arrays
        # stored in any attribute.

        arrays = []
        for a in x.__dict__.values():
            if isinstance(a, np.ndarray | np.generic):
                arrays.append(a)
        return arrays

    for a in _underlying_arrays(A):
        for b in _underlying_arrays(B):
            if np.may_share_memory(a, b):
                return True
    return False

