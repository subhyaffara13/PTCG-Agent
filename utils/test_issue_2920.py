
def test_issue_2920():
    n = Symbol('n', negative=True)
    assert sqrt(n).is_imaginary

