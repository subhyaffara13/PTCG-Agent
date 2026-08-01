
def test_hollow_rejection():
    eq = [x + 3, x + 4]
    assert cse(eq) == ([], eq)

