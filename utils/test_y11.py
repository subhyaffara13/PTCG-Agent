
def test_Y11():
    # => pi cot(pi s)   (0 < Re s < 1)   [Gradshteyn and Ryzhik 17.43(5)]
    x, s = symbols('x s')
    # raises RuntimeError: maximum recursion depth exceeded
    # https://github.com/sympy/sympy/issues/7181
    # Update 2019-02-17 raises:
    # TypeError: cannot unpack non-iterable MellinTransform object
    F, _, _ =  mellin_transform(1/(1 - x), x, s)
    assert F == pi*cot(pi*s)

