
def test_FractionField__init():
    F, = field("", ZZ)
    assert ZZ.frac_field() == F.to_domain()

