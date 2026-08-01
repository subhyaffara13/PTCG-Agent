
def test_ProductSet_of_single_arg_is_not_arg():
    assert unchanged(ProductSet, Interval(0, 1))
    assert unchanged(ProductSet, ProductSet(Interval(0, 1)))

