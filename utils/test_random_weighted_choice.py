
def test_random_weighted_choice():
    mapping = {"a": 10, "b": 0}
    c = nx.utils.weighted_choice(mapping, seed=1)
    c = nx.utils.weighted_choice(mapping)
    assert c == "a"

