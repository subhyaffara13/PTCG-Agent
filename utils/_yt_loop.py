
def _YT_loop(ker_pole, transfer_matrix, poles, B, maxiter, rtol):
    """
    Algorithm "YT" Tits, Yang. Globally Convergent
    Algorithms for Robust Pole Assignment by State Feedback
    https://hdl.handle.net/1903/5598
    The poles P have to be sorted accordingly to section 6.2 page 20

    """
    # The IEEE edition of the YT paper gives useful information on the
    # optimal update order for the real poles in order to minimize the number
    # of times we have to loop over all poles, see page 1442
    nb_real = poles[np.isreal(poles)].shape[0]
    # hnb => Half Nb Real
    hnb = nb_real // 2

    # Stick to the indices in the paper and then remove one to get numpy array
    # index it is a bit easier to link the code to the paper this way even if it
    # is not very clean. The paper is unclear about what should be done when
    # there is only one real pole => use KNV0 on this real pole seem to work
    if nb_real > 0:
        #update the biggest real pole with the smallest one
        update_order = [[nb_real], [1]]
    else:
        update_order = [[],[]]

    r_comp = np.arange(nb_real+1, len(poles)+1, 2)
    # step 1.a
    r_p = np.arange(1, hnb+nb_real % 2)
    update_order[0].extend(2*r_p)
    update_order[1].extend(2*r_p+1)
    # step 1.b
    update_order[0].extend(r_comp)
    update_order[1].extend(r_comp+1)
    # step 1.c
    r_p = np.arange(1, hnb+1)
    update_order[0].extend(2*r_p-1)
    update_order[1].extend(2*r_p)
    # step 1.d
    if hnb == 0 and np.isreal(poles[0]):
        update_order[0].append(1)
        update_order[1].append(1)
    update_order[0].extend(r_comp)
    update_order[1].extend(r_comp+1)
    # step 2.a
    r_j = np.arange(2, hnb+nb_real % 2)
    for j in r_j:
        for i in range(1, hnb+1):
            update_order[0].append(i)
            update_order[1].append(i+j)
    # step 2.b
    if hnb == 0 and np.isreal(poles[0]):
        update_order[0].append(1)
        update_order[1].append(1)
    update_order[0].extend(r_comp)
    update_order[1].extend(r_comp+1)
    # step 2.c
    r_j = np.arange(2, hnb+nb_real % 2)
    for j in r_j:
        for i in range(hnb+1, nb_real+1):
            idx_1 = i+j
            if idx_1 > nb_real:
                idx_1 = i+j-nb_real
            update_order[0].append(i)
            update_order[1].append(idx_1)
    # step 2.d
    if hnb == 0 and np.isreal(poles[0]):
        update_order[0].append(1)
        update_order[1].append(1)
    update_order[0].extend(r_comp)
    update_order[1].extend(r_comp+1)
    # step 3.a
    for i in range(1, hnb+1):
        update_order[0].append(i)
        update_order[1].append(i+hnb)
    # step 3.b
    if hnb == 0 and np.isreal(poles[0]):
        update_order[0].append(1)
        update_order[1].append(1)
    update_order[0].extend(r_comp)
    update_order[1].extend(r_comp+1)

    update_order = np.array(update_order).T-1
    stop = False
    nb_try = 0
    while nb_try < maxiter and not stop:
        det_transfer_matrixb = np.abs(np.linalg.det(transfer_matrix))
        for i, j in update_order:
            if i == j:
                assert i == 0, "i!=0 for KNV call in YT"
                assert np.isreal(poles[i]), "calling KNV on a complex pole"
                _KNV0(B, ker_pole, transfer_matrix, i, poles)
            else:
                transfer_matrix_not_i_j = np.delete(transfer_matrix, (i, j),
                                                    axis=1)
                # after merge of gh-4249 great speed improvements could be
                # achieved using QR updates instead of full QR in the line below

                #to debug with numpy qr uncomment the line below
                #Q, _ = np.linalg.qr(transfer_matrix_not_i_j, mode="complete")
                Q, _ = s_qr(transfer_matrix_not_i_j, mode="full")

                if np.isreal(poles[i]):
                    assert np.isreal(poles[j]), "mixing real and complex " + \
                        "in YT_real" + str(poles)
                    _YT_real(ker_pole, Q, transfer_matrix, i, j)
                else:
                    assert ~np.isreal(poles[i]), "mixing real and complex " + \
                        "in YT_real" + str(poles)
                    _YT_complex(ker_pole, Q, transfer_matrix, i, j)

        det_transfer_matrix = np.max((np.sqrt(np.spacing(1)),
                                  np.abs(np.linalg.det(transfer_matrix))))
        cur_rtol = np.abs(
            (det_transfer_matrix -
             det_transfer_matrixb) /
            det_transfer_matrix)
        if cur_rtol < rtol and det_transfer_matrix > np.sqrt(np.spacing(1)):
            # Convergence test from YT page 21
            stop = True
        nb_try += 1
    return stop, cur_rtol, nb_try

