
def _KNV0(B, ker_pole, transfer_matrix, j, poles):
    """
    Algorithm "KNV0" Kautsky et Al. Robust pole
    assignment in linear state feedback, Int journal of Control
    1985, vol 41 p 1129->1155
    https://la.epfl.ch/files/content/sites/la/files/
        users/105941/public/KautskyNicholsDooren

    """
    # Remove xj form the base
    transfer_matrix_not_j = np.delete(transfer_matrix, j, axis=1)
    # If we QR this matrix in full mode Q=Q0|Q1
    # then Q1 will be a single column orthogonal to
    # Q0, that's what we are looking for !

    # After merge of gh-4249 great speed improvements could be achieved
    # using QR updates instead of full QR in the line below

    # To debug with numpy qr uncomment the line below
    # Q, R = np.linalg.qr(transfer_matrix_not_j, mode="complete")
    Q, R = s_qr(transfer_matrix_not_j, mode="full")

    mat_ker_pj = np.dot(ker_pole[j], ker_pole[j].T)
    yj = np.dot(mat_ker_pj, Q[:, -1])

    # If Q[:, -1] is "almost" orthogonal to ker_pole[j] its
    # projection into ker_pole[j] will yield a vector
    # close to 0.  As we are looking for a vector in ker_pole[j]
    # simply stick with transfer_matrix[:, j] (unless someone provides me with
    # a better choice ?)

    if not np.allclose(yj, 0):
        xj = yj/np.linalg.norm(yj)
        transfer_matrix[:, j] = xj

