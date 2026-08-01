
def test_fps__slow():
    f = x*exp(x)*sin(2*x)  # TODO: rsolve needs improvement
    assert fps(f, x).truncate() == 2*x**2 + 2*x**3 - x**4/3 - x**5 + O(x**6)

