
def reconstruct_interp_matrix(idx, proj):
    """
    Reconstruct interpolation matrix from ID.

    The interpolation matrix can be reconstructed from the ID indices and
    coefficients `idx` and `proj`, respectively, as::

        P = numpy.hstack([numpy.eye(proj.shape[0]), proj])[:,numpy.argsort(idx)]

    The original matrix can then be reconstructed from its skeleton matrix ``B``
    via ``A = B @ P``

    See also :func:`reconstruct_matrix_from_id` and
    :func:`reconstruct_skel_matrix`.

    ..  This function automatically detects the matrix data type and calls the
        appropriate backend. For details, see :func:`_backend.idd_reconint` and
        :func:`_backend.idz_reconint`.

    Parameters
    ----------
    idx : :class:`numpy.ndarray`
        1D column index array.
    proj : :class:`numpy.ndarray`
        Interpolation coefficients.

    Returns
    -------
    :class:`numpy.ndarray`
        Interpolation matrix.
    """
    n, krank = len(idx), proj.shape[0]
    if _is_real(proj):
        p = np.zeros([krank, n], dtype=np.float64)
    else:
        p = np.zeros([krank, n], dtype=np.complex128)

    for ci in range(krank):
        p[ci, idx[ci]] = 1.0
    p[:, idx[krank:]] = proj[:, :]

    return p

