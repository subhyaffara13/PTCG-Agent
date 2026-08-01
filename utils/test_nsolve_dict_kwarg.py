
def test_nsolve_dict_kwarg():
    x, y = symbols('x y')
    # one variable
    assert nsolve(x**2 - 2, 1, dict = True) == \
        [{x: sqrt(2.)}]
    # one variable with complex solution
    assert nsolve(x**2 + 2, I, dict = True) == \
        [{x: sqrt(2.)*I}]
    # two variables
    assert nsolve([x**2 + y**2 - 5, x**2 - y**2 + 1], [x, y], [1, 1], dict = True) == \
        [{x: sqrt(2.), y: sqrt(3.)}]

