
def test_order_conjugate_transpose():
    x = Symbol('x', real=True)
    y = Symbol('y', imaginary=True)
    assert conjugate(Order(x)) == Order(conjugate(x))
    assert conjugate(Order(y)) == Order(conjugate(y))
    assert conjugate(Order(x**2)) == Order(conjugate(x)**2)
    assert conjugate(Order(y**2)) == Order(conjugate(y)**2)
    assert transpose(Order(x)) == Order(transpose(x))
    assert transpose(Order(y)) == Order(transpose(y))
    assert transpose(Order(x**2)) == Order(transpose(x)**2)
    assert transpose(Order(y**2)) == Order(transpose(y)**2)

