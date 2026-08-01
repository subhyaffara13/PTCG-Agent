
def _coo_gen_triples(A):
    """Converts a SciPy sparse array in **Coordinate** format to an iterable
    of weighted edge triples.

    """
    return zip(A.row.tolist(), A.col.tolist(), A.data.tolist())

