
def test_rewrite_trig():
    assert solve(sin(x) + tan(x)) == [0, -pi, pi, 2*pi]
    assert solve(sin(x) + sec(x)) == [
        -2*atan(Rational(-1, 2) + sqrt(2)*sqrt(1 - sqrt(3)*I)/2 + sqrt(3)*I/2),
        2*atan(S.Half - sqrt(2)*sqrt(1 + sqrt(3)*I)/2 + sqrt(3)*I/2), 2*atan(S.Half
        + sqrt(2)*sqrt(1 + sqrt(3)*I)/2 + sqrt(3)*I/2), 2*atan(S.Half -
        sqrt(3)*I/2 + sqrt(2)*sqrt(1 - sqrt(3)*I)/2)]
    assert solve(sinh(x) + tanh(x)) == [0, I*pi]

    # issue 6157
    assert solve(2*sin(x) - cos(x), x) == [atan(S.Half)]

