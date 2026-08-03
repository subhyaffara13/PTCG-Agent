import itertools

def test_form_qTu():
    # We want to ensure that all of the code paths through this function are
    # tested. Most of them should be hit with the rest of test suite, but
    # explicit tests make clear precisely what is being tested.
    #
    # This function expects that Q is either C or F contiguous and square.
    # Economic mode decompositions (Q is (M, N), M != N) do not go through this
    # function. U may have any positive strides.
    #
    # Some of these test are duplicates, since contiguous 1d arrays are both C
    # and F.

    q_order = ['F', 'C']
    q_shape = [(8, 8), ]
    u_order = ['F', 'C', 'A']  # here A means is not F not C
    u_shape = [1, 3]
    dtype = ['f', 'd', 'F', 'D']

    for qo, qs, uo, us, d in \
            itertools.product(q_order, q_shape, u_order, u_shape, dtype):
        if us == 1:
            check_form_qTu(qo, qs, uo, us, 1, d)
            check_form_qTu(qo, qs, uo, us, 2, d)
        else:
            check_form_qTu(qo, qs, uo, us, 2, d)

