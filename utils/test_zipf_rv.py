
def test_zipf_rv():
    r = nx.utils.zipf_rv(2.3, xmin=2, seed=1)
    r = nx.utils.zipf_rv(2.3, 2, 1)
    r = nx.utils.zipf_rv(2.3)
    assert type(r), int
    pytest.raises(ValueError, nx.utils.zipf_rv, 0.5)
    pytest.raises(ValueError, nx.utils.zipf_rv, 2, xmin=0)

