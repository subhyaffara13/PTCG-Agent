
def test_Quantity_str():
    assert sstr(second, abbrev=True) == "s"
    assert sstr(joule, abbrev=True) == "J"
    assert str(second) == "second"
    assert str(joule) == "joule"

