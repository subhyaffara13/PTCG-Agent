
def read_unformatted_mixed(m, n, k, filename):
    """
    Read a Fortran unformatted binary file that contains a mix of:
    - a double precision array a(m, n)
    - an integer array b(k)

    Assumes a single write(10) a, b was used and file is wrapped
    with Fortran record markers.

    Returns:
        a: np.ndarray of shape (m, n) with dtype float64
        b: np.ndarray of shape (k,) with dtype int32

    Reference:
        Fortran implementation:
        https://github.com/scipy/scipy/blob/maintenance/1.15.x/scipy/io/_test_fortran.f#L21-L30
    """
    with open(filename.strip(), 'rb') as f:
        f.read(4)  # Skip initial 4-byte record marker

        # Read a(m,n): total m*n float64 values
        a_flat = np.fromfile(f, dtype=np.float64, count=m * n)

        # Read b(k): total k int32 values (assuming Fortran default integer*4)
        b = np.fromfile(f, dtype=np.int32, count=k)

        f.read(4)  # Skip trailing 4-byte record marker

    # Reshape a to (m,n) Fortran-style
    a = a_flat.reshape((m, n), order='F')

    return a, b

