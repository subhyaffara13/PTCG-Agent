
def test_issue_11099():
    from sympy.abc import x, y
    # some fixed value tests
    fixed_test_data = {x: -2, y: 3}
    assert Min(x, y).evalf(subs=fixed_test_data) == \
        Min(x, y).subs(fixed_test_data).evalf()
    assert Max(x, y).evalf(subs=fixed_test_data) == \
        Max(x, y).subs(fixed_test_data).evalf()
    # randomly generate some test data
    from sympy.core.random import randint
    for i in range(20):
        random_test_data = {x: randint(-100, 100), y: randint(-100, 100)}
        assert Min(x, y).evalf(subs=random_test_data) == \
            Min(x, y).subs(random_test_data).evalf()
        assert Max(x, y).evalf(subs=random_test_data) == \
            Max(x, y).subs(random_test_data).evalf()

