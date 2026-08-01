
def test_julia_piecewise_times_const():
    pw = Piecewise((x, x < 1), (x**2, True))
    assert julia_code(2*pw) == "2 * ((x < 1) ? (x) : (x .^ 2))"
    assert julia_code(pw/x) == "((x < 1) ? (x) : (x .^ 2)) ./ x"
    assert julia_code(pw/(x*y)) == "((x < 1) ? (x) : (x .^ 2)) ./ (x .* y)"
    assert julia_code(pw/3) == "((x < 1) ? (x) : (x .^ 2)) / 3"

