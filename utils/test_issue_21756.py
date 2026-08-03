import re

def test_issue_21756():
    term = (1 - exp(-2*I*pi*z))/(1 - exp(-2*I*pi*z/5))
    assert term.limit(z, 0) == 5
    assert re(term).limit(z, 0) == 5

