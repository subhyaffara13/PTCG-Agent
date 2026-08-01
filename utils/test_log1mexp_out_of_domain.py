
def test_log1mexp_out_of_domain(x):
    observed = _log1mexp(x)
    assert np.isnan(observed)

