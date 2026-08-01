
def test_issue_14027():
    assert integrate(1/(1 + exp(x - S.Half)/(1 + exp(x))), x) == \
        x - exp(S.Half)*log(exp(x) + exp(S.Half)/(1 + exp(S.Half)))/(exp(S.Half) + E)

