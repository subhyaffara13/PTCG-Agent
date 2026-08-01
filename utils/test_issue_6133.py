
def test_issue_6133():
    raises(TypeError, lambda: (-oo < None))
    raises(TypeError, lambda: (S(-2) < None))
    raises(TypeError, lambda: (oo < None))
    raises(TypeError, lambda: (oo > None))
    raises(TypeError, lambda: (S(2) < None))

