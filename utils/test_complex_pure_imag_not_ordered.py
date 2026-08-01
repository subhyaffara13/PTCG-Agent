
def test_complex_pure_imag_not_ordered():
    raises(TypeError, lambda: 2*I < 3*I)

    # more generally
    x = Symbol('x', real=True, nonzero=True)
    y = Symbol('y', imaginary=True)
    z = Symbol('z', complex=True)
    assert_all_ineq_raise_TypeError(I, y)

    t = I*x   # an imaginary number, should raise errors
    assert_all_ineq_raise_TypeError(2, t)

    t = -I*y   # a real number, so no errors
    assert_all_ineq_give_class_Inequality(2, t)

    t = I*z   # unknown, should be unevaluated
    assert_all_ineq_give_class_Inequality(2, t)

