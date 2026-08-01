
def test_output_arg_f():
    from sympy.core.relational import Equality
    from sympy.functions.elementary.trigonometric import (cos, sin)
    x, y, z = symbols("x,y,z")
    r = make_routine("foo", [Equality(y, sin(x)), cos(x)])
    c = FCodeGen()
    result = c.write([r], "test", header=False, empty=False)
    assert result[0][0] == "test.f90"
    assert result[0][1] == (
        'REAL*8 function foo(x, y)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'REAL*8, intent(out) :: y\n'
        'y = sin(x)\n'
        'foo = cos(x)\n'
        'end function\n'
    )

