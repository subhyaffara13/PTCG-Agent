
def test_M12():
    # TODO: x = [-1, 2*(+/-asinh(1)*I + n*pi}, 3*(pi/6 + n*pi/3)]
    # TODO: Replace solve with solveset, as of now test fails for solveset
    assert solve((x + 1)*(sin(x)**2 + 1)**2*cos(3*x)**3, x) == [
        -1, pi/6, pi/2,
           - I*log(1 + sqrt(2)),      I*log(1 + sqrt(2)),
        pi - I*log(1 + sqrt(2)), pi + I*log(1 + sqrt(2)),
    ]

