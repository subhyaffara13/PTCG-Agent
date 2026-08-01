
def test_H26():
    g = expand((sin(x) - 2*cos(y)**2 + 3*tan(z)**3)**20)
    assert factor(g, expand=False) == (-sin(x) + 2*cos(y)**2 - 3*tan(z)**3)**20

