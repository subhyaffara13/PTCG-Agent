
def test_issue_14721():
    k, h, a, b = symbols(':4')
    assert solve([
        -1 + (-k + 1)**2/b**2 + (-h - 1)**2/a**2,
        -1 + (-k + 1)**2/b**2 + (-h + 1)**2/a**2,
        h, k + 2], h, k, a, b) == [
        (0, -2, -b*sqrt(1/(b**2 - 9)), b),
        (0, -2, b*sqrt(1/(b**2 - 9)), b)]
    assert solve([
        h, h/a + 1/b**2 - 2, -h/2 + 1/b**2 - 2], a, h, b) == [
        (a, 0, -sqrt(2)/2), (a, 0, sqrt(2)/2)]
    assert solve((a + b**2 - 1, a + b**2 - 2)) == []

