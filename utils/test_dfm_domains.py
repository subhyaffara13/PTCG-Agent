
def test_DFM_domains():
    """Test which domains are supported by DFM."""

    x, y = symbols('x, y')

    if GROUND_TYPES in ('python', 'gmpy'):

        supported = []
        flint_funcs = {}
        not_supported = [ZZ, QQ, GF(5), QQ[x], QQ[x,y]]

    elif GROUND_TYPES == 'flint':

        import flint
        supported = [ZZ, QQ]
        flint_funcs = {
            ZZ: flint.fmpz_mat,
            QQ: flint.fmpq_mat,
            GF(5): None,
        }
        not_supported = [
            # Other domains could be supported but not implemented as matrices
            # in python-flint:
            QQ[x],
            QQ[x,y],
            QQ.frac_field(x,y),
            # Others would potentially never be supported by python-flint:
            ZZ_I,
        ]

    else:
        assert False, "Unknown GROUND_TYPES: %s" % GROUND_TYPES

    for domain in supported:
        assert DFM._supports_domain(domain) is True
        if flint_funcs[domain] is not None:
            assert DFM._get_flint_func(domain) == flint_funcs[domain]
    for domain in not_supported:
        assert DFM._supports_domain(domain) is False
        raises(NotImplementedError, lambda: DFM._get_flint_func(domain))

