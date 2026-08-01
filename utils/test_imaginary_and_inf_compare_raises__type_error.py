
def test_imaginary_and_inf_compare_raises_TypeError():
    # See pull request #7835
    y = Symbol('y', imaginary=True)
    assert_all_ineq_raise_TypeError(oo, y)
    assert_all_ineq_raise_TypeError(-oo, y)

