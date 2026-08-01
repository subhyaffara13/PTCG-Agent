
def test_double_negation():
    a = Boolean()
    assert ~(~a) == a

