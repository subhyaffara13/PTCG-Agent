
def test_fcode_For():
    x, y = symbols('x y')

    f = For(x, Range(0, 10, 2), [Assignment(y, x * y)])
    sol = fcode(f)
    assert sol == ("      do x = 0, 9, 2\n"
                   "         y = x*y\n"
                   "      end do")

