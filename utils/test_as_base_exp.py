
def test_as_base_exp():
    assert x.as_base_exp() == (x, S.One)
    assert (x*y*z).as_base_exp() == (x*y*z, S.One)
    assert (x + y + z).as_base_exp() == (x + y + z, S.One)
    assert ((x + y)**z).as_base_exp() == (x + y, z)
    assert (x**2*y**2).as_base_exp() == (x*y, 2)
    assert (x**z*y**z).as_base_exp() == (x**z*y**z, S.One)

