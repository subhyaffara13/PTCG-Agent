
def test_issue_5653():
    assert sqrtdenest(
        sqrt(2 + sqrt(2 + sqrt(2)))) == sqrt(2 + sqrt(2 + sqrt(2)))

