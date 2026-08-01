
def test_issue_7180():
    assert latex(Equivalent(x, y)) == r"x \Leftrightarrow y"
    assert latex(Not(Equivalent(x, y))) == r"x \not\Leftrightarrow y"


def test_issue_7180():
    assert upretty(Equivalent(x, y)) == 'x ⇔ y'

