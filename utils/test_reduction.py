
def test_reduction():
    from sympy.polys.distributedmodules import sdm_nf_buchberger_reduced
    R = QQ.old_poly_ring(x, y)
    I = R.ideal(x**5, y)
    e = R.convert(x**3 + y**2)
    assert I.reduce_element(e) == e
    assert I.reduce_element(e, NF=sdm_nf_buchberger_reduced) == R.convert(x**3)


def test_reduction(name):
    """Test that the elements of the rotation group are correctly
    mapped onto the identity rotation."""
    g = Rotation.create_group(name)
    f = g.reduce(g)
    assert_array_almost_equal(f.magnitude(), np.zeros(len(g)))

