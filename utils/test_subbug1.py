
def test_subbug1():
    # see that they don't fail
    (x**x).subs(x, 1)
    (x**x).subs(x, 1.0)

