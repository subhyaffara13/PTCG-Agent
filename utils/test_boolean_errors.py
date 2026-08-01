
def test_boolean_errors():
    a = intervalMembership(True, True)
    raises(ValueError, lambda: a & 1)
    raises(ValueError, lambda: a | 1)
    raises(ValueError, lambda: a ^ 1)

