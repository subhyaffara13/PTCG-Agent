
def test_random_weighted_sample():
    mapping = {"a": 10, "b": 20}
    s = nx.utils.random_weighted_sample(mapping, 2, seed=1)
    s = nx.utils.random_weighted_sample(mapping, 2)
    assert sorted(s) == sorted(mapping.keys())
    pytest.raises(ValueError, nx.utils.random_weighted_sample, mapping, 3)

