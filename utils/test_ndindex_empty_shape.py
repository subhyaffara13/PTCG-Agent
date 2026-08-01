
def test_ndindex_empty_shape():
    import numpy as np
    # ndindex() and ndindex(()) should return a single empty tuple
    assert list(np.ndindex()) == [()]
    assert list(np.ndindex(())) == [()]

