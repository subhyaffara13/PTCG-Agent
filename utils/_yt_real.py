
def _YT_real(ker_pole, Q, transfer_matrix, i, j):
    """
    Applies algorithm from YT section 6.1 page 19 related to real pairs
    """
    # step 1 page 19
    u = Q[:, -2, np.newaxis]
    v = Q[:, -1, np.newaxis]

    # step 2 page 19
    m = np.dot(np.dot(ker_pole[i].T, np.dot(u, v.T) -
        np.dot(v, u.T)), ker_pole[j])

    # step 3 page 19
    um, sm, vm = np.linalg.svd(m)
    # mu1, mu2 two first columns of U => 2 first lines of U.T
    mu1, mu2 = um.T[:2, :, np.newaxis]
    # VM is V.T with numpy we want the first two lines of V.T
    nu1, nu2 = vm[:2, :, np.newaxis]

    # what follows is a rough python translation of the formulas
    # in section 6.2 page 20 (step 4)
    transfer_matrix_j_mo_transfer_matrix_j = np.vstack((
            transfer_matrix[:, i, np.newaxis],
            transfer_matrix[:, j, np.newaxis]))

    if not np.allclose(sm[0], sm[1]):
        ker_pole_imo_mu1 = np.dot(ker_pole[i], mu1)
        ker_pole_i_nu1 = np.dot(ker_pole[j], nu1)
        ker_pole_mu_nu = np.vstack((ker_pole_imo_mu1, ker_pole_i_nu1))
    else:
        ker_pole_ij = np.vstack((
                                np.hstack((ker_pole[i],
                                           np.zeros(ker_pole[i].shape))),
                                np.hstack((np.zeros(ker_pole[j].shape),
                                                    ker_pole[j]))
                                ))
        mu_nu_matrix = np.vstack(
            (np.hstack((mu1, mu2)), np.hstack((nu1, nu2)))
            )
        ker_pole_mu_nu = np.dot(ker_pole_ij, mu_nu_matrix)
    transfer_matrix_ij = np.dot(np.dot(ker_pole_mu_nu, ker_pole_mu_nu.T),
                             transfer_matrix_j_mo_transfer_matrix_j)
    if not np.allclose(transfer_matrix_ij, 0):
        transfer_matrix_ij = (np.sqrt(2)*transfer_matrix_ij /
                              np.linalg.norm(transfer_matrix_ij))
        transfer_matrix[:, i] = transfer_matrix_ij[
            :transfer_matrix[:, i].shape[0], 0
            ]
        transfer_matrix[:, j] = transfer_matrix_ij[
            transfer_matrix[:, i].shape[0]:, 0
            ]
    else:
        # As in knv0 if transfer_matrix_j_mo_transfer_matrix_j is orthogonal to
        # Vect{ker_pole_mu_nu} assign transfer_matrixi/transfer_matrix_j to
        # ker_pole_mu_nu and iterate. As we are looking for a vector in
        # Vect{Matker_pole_MU_NU} (see section 6.1 page 19) this might help
        # (that's a guess, not a claim !)
        transfer_matrix[:, i] = ker_pole_mu_nu[
            :transfer_matrix[:, i].shape[0], 0
            ]
        transfer_matrix[:, j] = ker_pole_mu_nu[
            transfer_matrix[:, i].shape[0]:, 0
            ]

