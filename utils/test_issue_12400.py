
def test_issue_12400():
    # Correction of check for negative exponents
    assert poly(1/(1+sqrt(2)), x) == \
            Poly(1/(1+sqrt(2)), x, domain='EX')

