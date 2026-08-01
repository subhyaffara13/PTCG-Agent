
def test_perfect():
    G = AlternatingGroup(3)
    assert G.is_perfect is False
    G = AlternatingGroup(5)
    assert G.is_perfect is True

