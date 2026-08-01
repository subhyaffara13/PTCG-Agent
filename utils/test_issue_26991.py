
def test_issue_26991():
    assert limit(x/((x - 6)*sinh(tanh(0.03*x)) + tanh(x) - 0.5), x, oo) == 1/sinh(1)

