
def test_ncfdtri_domain_error(args):
    with sp.errstate(domain="raise"):
        with pytest.raises(sp.SpecialFunctionError, match="domain"):
            sp.ncfdtri(*args)

