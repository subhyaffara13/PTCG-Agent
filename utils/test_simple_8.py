
def test_simple_8():
    assert O(sqrt(-x)) == O(sqrt(x))
    assert O(x**2*sqrt(x)) == O(x**Rational(5, 2))
    assert O(x**3*sqrt(-(-x)**3)) == O(x**Rational(9, 2))
    assert O(x**Rational(3, 2)*sqrt((-x)**3)) == O(x**3)
    assert O(x*(-2*x)**(I/2)) == O(x*(-x)**(I/2))

