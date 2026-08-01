
def test_evalf_real_alg_num():
    # This test demonstrates why the entry for `AlgebraicNumber` in
    # `sympy.core.evalf._create_evalf_table()` has to use `x.to_root()`,
    # instead of `x.as_expr()`. If the latter is used, then `z` will be
    # a complex number with `0.e-20` for imaginary part, even though `a5`
    # is a real number.
    zeta = Symbol('zeta')
    a5 = AlgebraicNumber(CRootOf(cyclotomic_poly(5), -1), [-1, -1, 0, 0], alias=zeta)
    z = a5.evalf()
    assert isinstance(z, Float)
    assert not hasattr(z, '_mpc_')
    assert hasattr(z, '_mpf_')

