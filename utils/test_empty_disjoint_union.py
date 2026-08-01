
def test_empty_disjoint_union():
    with pytest.raises(ValueError):
        nx.disjoint_union_all([])

