
def test_svd_test_case():
    # a test case from Golub and Reinsch
    #  (see wilkinson/reinsch: handbook for auto. comp., vol ii-linear algebra, 134-151(1971).)

    eps = mp.exp(0.8 * mp.log(mp.eps))

    a = [[22, 10,  2,   3,  7],
         [14,  7, 10,   0,  8],
         [-1, 13, -1, -11,  3],
         [-3, -2, 13,  -2,  4],
         [ 9,  8,  1,  -2,  4],
         [ 9,  1, -7,   5, -1],
         [ 2, -6,  6,   5,  1],
         [ 4,  5,  0,  -2,  2]]

    a = mp.matrix(a)
    b = mp.matrix([mp.sqrt(1248), 20, mp.sqrt(384), 0, 0])

    S = mp.svd_r(a, compute_uv = False)
    S -= b
    assert mp.mnorm(S) < eps

    S = mp.svd_c(a, compute_uv = False)
    S -= b
    assert mp.mnorm(S) < eps

