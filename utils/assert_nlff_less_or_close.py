
def assert_nlff_less_or_close(dist, data, params1, params0, rtol=1e-7, atol=0,
                              nlff_name='nnlf'):
    nlff = getattr(dist, nlff_name)
    nlff1 = nlff(params1, data)
    nlff0 = nlff(params0, data)
    if not (nlff1 < nlff0):
        np.testing.assert_allclose(nlff1, nlff0, rtol=rtol, atol=atol)

