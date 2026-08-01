
def test_empty_intersection_all():
    with pytest.raises(ValueError):
        nx.intersection_all([])

