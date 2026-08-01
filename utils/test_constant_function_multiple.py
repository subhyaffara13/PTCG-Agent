
def test_constant_function_multiple():
    # The rules to not renumber in this case would be too complicated, and
    # dsolve is not likely to ever encounter anything remotely like this.
    assert constant_renumber(
        constantsimp(f(C1, C1, x), [C1])) == f(C1, C1, x)

