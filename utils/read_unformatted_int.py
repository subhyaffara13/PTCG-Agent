
def read_unformatted_int(m, n, k, filename):
    """
    Read a Fortran unformatted binary file
    containing a 3D integer array (m, n, k).
    Assumes the array is written with a single
    write(10) a and wrapped with record markers.

    Returns:
        np.ndarray: 3D array of shape (m, n, k) with dtype int32

    Reference:
        Fortran implementation:
        https://github.com/scipy/scipy/blob/maintenance/1.15.x/scipy/io/_test_fortran.f#L11-L19
    """
    with open(filename.strip(), 'rb') as f:
        f.read(4)  # Skip Fortran record marker at start

        # Read m*n*k integers (Fortran default = 4 bytes per integer)
        data = np.fromfile(f, dtype=np.int32, count=m * n * k)

        f.read(4)  # Skip Fortran record marker at end

    if data.size != m * n * k:
        raise ValueError(f"Expected {m*n*k} elements, got {data.size}")

    return data.reshape((m, n, k), order='F')  # Fortran-style column-major order

