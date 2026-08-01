
def _csr_gen_triples(A):
    """Converts a SciPy sparse array in **Compressed Sparse Row** format to
    an iterable of weighted edge triples.

    """
    nrows = A.shape[0]
    indptr, dst_indices, data = A.indptr, A.indices, A.data
    import numpy as np

    src_indices = np.repeat(np.arange(nrows), np.diff(indptr))
    return zip(src_indices.tolist(), dst_indices.tolist(), A.data.tolist())

