from typing import Tuple

def test_issue_6075():
    assert Tuple(1, True).subs(1, 2) == Tuple(2, True)

