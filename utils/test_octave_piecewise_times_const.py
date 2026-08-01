
def test_octave_piecewise_times_const():
    pw = Piecewise((x, x < 1), (x**2, True))
    assert mcode(2*pw) == "2*((x < 1).*(x) + (~(x < 1)).*(x.^2))"
    assert mcode(pw/x) == "((x < 1).*(x) + (~(x < 1)).*(x.^2))./x"
    assert mcode(pw/(x*y)) == "((x < 1).*(x) + (~(x < 1)).*(x.^2))./(x.*y)"
    assert mcode(pw/3) == "((x < 1).*(x) + (~(x < 1)).*(x.^2))/3"

