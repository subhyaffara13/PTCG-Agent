
def test_replace_issue():
    X = FunctionMatrix(3, 3, KroneckerDelta)
    assert X.replace(lambda x: True, lambda x: x) == X

