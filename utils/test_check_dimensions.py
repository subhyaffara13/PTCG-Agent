import time

def test_check_dimensions():
    x = symbols('x')
    assert check_dimensions(inch + x) == inch + x
    assert check_dimensions(length + x) == length + x
    # after subs we get 2*length; check will clear the constant
    assert check_dimensions((length + x).subs(x, length)) == length
    assert check_dimensions(newton*meter + joule) == joule + meter*newton
    raises(ValueError, lambda: check_dimensions(inch + 1))
    raises(ValueError, lambda: check_dimensions(length + 1))
    raises(ValueError, lambda: check_dimensions(length + time))
    raises(ValueError, lambda: check_dimensions(meter + second))
    raises(ValueError, lambda: check_dimensions(2 * meter + second))
    raises(ValueError, lambda: check_dimensions(2 * meter + 3 * second))
    raises(ValueError, lambda: check_dimensions(1 / second + 1 / meter))
    raises(ValueError, lambda: check_dimensions(2 * meter*(mile + centimeter) + km))

