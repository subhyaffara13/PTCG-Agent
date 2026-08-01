
def test_nbinom_11465(mu, q, expected):
    # test nbinom.logcdf at extreme tails
    size = 20
    n, p = size, size/(size+mu)
    # In R:
    # options(digits=16)
    # pnbinom(mu=10, size=20, q=120, log.p=TRUE)
    assert_allclose(nbinom.logcdf(q, n, p), expected)

