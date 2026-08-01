
def test_issue_4313():
    u = Piecewise((0, x <= 0), (1, x >= a), (x/a, True))
    e = (u - u.subs(x, y))**2/(x - y)**2
    M = Max(0, a)
    assert integrate(e,  x).expand() == Piecewise(
        (Piecewise(
            (0, x <= 0),
            (-y**2/(a**2*x - a**2*y) + x/a**2 - 2*y*log(-y)/a**2 +
                2*y*log(x - y)/a**2 - y/a**2, x <= M),
            (-y**2/(-a**2*y + a**2*M) + 1/(-y + M) -
                1/(x - y) - 2*y*log(-y)/a**2 + 2*y*log(-y +
                M)/a**2 - y/a**2 + M/a**2, True)),
        ((a <= y) & (y <= 0)) | ((y <= 0) & (y > -oo))),
        (Piecewise(
            (-1/(x - y), x <= 0),
            (-a**2/(a**2*x - a**2*y) + 2*a*y/(a**2*x - a**2*y) -
                y**2/(a**2*x - a**2*y) + 2*log(-y)/a - 2*log(x - y)/a +
                2/a + x/a**2 - 2*y*log(-y)/a**2 + 2*y*log(x - y)/a**2 -
                y/a**2, x <= M),
            (-a**2/(-a**2*y + a**2*M) + 2*a*y/(-a**2*y +
                a**2*M) - y**2/(-a**2*y + a**2*M) +
                2*log(-y)/a - 2*log(-y + M)/a + 2/a -
                2*y*log(-y)/a**2 + 2*y*log(-y + M)/a**2 -
                y/a**2 + M/a**2, True)),
        a <= y),
        (Piecewise(
            (-y**2/(a**2*x - a**2*y), x <= 0),
            (x/a**2 + y/a**2, x <= M),
            (a**2/(-a**2*y + a**2*M) -
                a**2/(a**2*x - a**2*y) - 2*a*y/(-a**2*y + a**2*M) +
                2*a*y/(a**2*x - a**2*y) + y**2/(-a**2*y + a**2*M) -
                y**2/(a**2*x - a**2*y) + y/a**2 + M/a**2, True)),
        True))

