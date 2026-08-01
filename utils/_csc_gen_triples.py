
def _csc_gen_triples(A):
    """Converts a SciPy sparse array in **Compressed Sparse Column** format to
    an iterable of weighted edge triples.

    """
    ncols = A.shape[1]
    indptr, src_indices, data = A.indptr, A.indices, A.data
    import numpy as np

    dst_indices = np.repeat(np.arange(ncols), np.diff(indptr))
    return zip(src_indices.tolist(), dst_indices.tolist(), A.data.tolist())

