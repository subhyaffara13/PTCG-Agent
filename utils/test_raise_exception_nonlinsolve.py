
def test_raise_exception_nonlinsolve():
    raises(IndexError, lambda: nonlinsolve([x**2 -1], []))
    raises(ValueError, lambda: nonlinsolve([x**2 -1]))

