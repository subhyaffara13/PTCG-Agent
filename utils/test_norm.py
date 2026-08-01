
def test_norm():
    a, b = sqrt(2), sqrt(3)
    f = Poly(a*x + b*y, x, y, extension=(a, b))
    assert f.norm() == Poly(4*x**4 - 12*x**2*y**2 + 9*y**4, x, y, domain='QQ')


def test_norm():
    # Maximum "n" which is tested:
    n_max = 2  # it works, but is slow, for n_max > 2
    for n in range(n_max + 1):
        for l in range(n):
            assert integrate(R_nl(n, l, r)**2 * r**2, (r, 0, oo)) == 1


def test_norm(n=1):
    # Maximum "n" which is tested:
    for i in range(n + 1):
        assert integrate(
            wavefunction(i, x) * wavefunction(-i, x), (x, 0, 2 * pi)) == 1


def test_norm(n=1):
    # Maximum "n" which is tested:
    for i in range(n + 1):
        assert integrate(psi_n(i, x, 1, 1)**2, (x, -oo, oo)) == 1


def test_norm():
    """
    Test fitting the normal distribution to interval-censored data.

    Calculation in R:

    > library(fitdistrplus)
    > data <- data.frame(left=c(0.10, 0.50, 0.75, 0.80),
    +                    right=c(0.20, 0.55, 0.90, 0.95))
    > result = fitdistcens(data, 'norm', control=list(reltol=1e-14))

    > result
    Fitting of the distribution ' norm ' on censored data by maximum likelihood
    Parameters:
          estimate
    mean 0.5919990
    sd   0.2868042
    > result$sd
         mean        sd
    0.1444432 0.1029451
    """
    data = CensoredData(interval=[[0.10, 0.20],
                                  [0.50, 0.55],
                                  [0.75, 0.90],
                                  [0.80, 0.95]])

    loc, scale = norm.fit(data, optimizer=optimizer)

    assert_allclose(loc, 0.5919990, rtol=5e-6)
    assert_allclose(scale, 0.2868042, rtol=5e-6)


def test_norm(A):
    C = spla.norm(A)
    npt.assert_allclose(C, np.linalg.norm(A.todense()))


def test_norm(matrices):
    A_dense, A_sparse, b = matrices
    norm0 = splin.norm(sp.csr_array(A_dense))
    norm = splin.norm(A_sparse)
    assert_allclose(norm, norm0)

