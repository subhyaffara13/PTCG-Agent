
def test_negative_input():
    assert not nx.is_graphical([-1], "hh")
    assert not nx.is_graphical([-1], "eg")

