
def test_issue_20163():
    assert apart(1/(x**6+1), extension=[sqrt(3), I]) == \
        (sqrt(3) + I)/(2*x + sqrt(3) + I)/6 + \
        (sqrt(3) - I)/(2*x + sqrt(3) - I)/6 - \
        (sqrt(3) - I)/(2*x - sqrt(3) + I)/6 - \
        (sqrt(3) + I)/(2*x - sqrt(3) - I)/6 + \
        I/(x + I)/6 - I/(x - I)/6

