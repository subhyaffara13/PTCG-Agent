
def test_issue_8945():
    assert integrate(sin(x)**3/x, (x, 0, 1)) == -Si(3)/4 + 3*Si(1)/4
    assert integrate(sin(x)**3/x, (x, 0, oo)) == pi/4
    assert integrate(cos(x)**2/x**2, x) == -Si(2*x) - cos(2*x)/(2*x) - 1/(2*x)

