
def test_sympy__functions__special__hyper__meijerg():
    from sympy.functions.special.hyper import meijerg
    assert _test_args(meijerg([1, 2, 3], [4, 5], [6], [], x))

