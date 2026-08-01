
def test_rbf_epsilon_none():
    x = linspace(0, 10, 9)
    y = sin(x)
    Rbf(x, y, epsilon=None)

