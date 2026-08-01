
def _dok_gen_triples(A):
    """Converts a SciPy sparse array in **Dictionary of Keys** format to an
    iterable of weighted edge triples.

    """
    for (r, c), v in A.items():
        # Use `v.item()` to convert a NumPy scalar to the appropriate Python scalar
        yield int(r), int(c), v.item()

