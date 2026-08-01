
def test_product_irrational():
    assert (I*pi).is_irrational is False
    # The following used to be deduced from the above bug:
    assert (I*pi).is_positive is False

