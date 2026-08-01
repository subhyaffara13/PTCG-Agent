
def read_unformatted_double(m, n, k, filename):
    """
    Read a Fortran-style unformatted binary file written with a single write() call,
    assuming it wraps the data with 4-byte record markers.

    Returns:
        np.ndarray of shape (m, n, k) with dtype float64

    Reference:
        Fortran implementation:
        https://github.com/scipy/scipy/blob/maintenance/1.15.x/scipy/io/_test_fortran.f#L1-L9
    """
    with open(filename.strip(), 'rb') as f:
        f.read(4)  # Skip initial 4-byte record marker
        data = np.fromfile(f, dtype=np.float64, count=m * n * k)
        f.read(4)  # Skip trailing 4-byte record marker

    if data.size != m * n * k:
        raise ValueError(f"Expected {m*n*k} elements, got {data.size}")

    return data.reshape((m, n, k), order='F')  # Fortran column-major order

