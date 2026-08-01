
def test_imaginary_compare_raises_TypeError():
    # See issue #5724
    assert_all_ineq_raise_TypeError(I, x)

