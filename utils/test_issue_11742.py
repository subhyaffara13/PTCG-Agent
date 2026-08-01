
def test_issue_11742():
    assert integrate(sqrt(-x**2 + 8*x + 48), (x, 4, 12)) == 16*pi

