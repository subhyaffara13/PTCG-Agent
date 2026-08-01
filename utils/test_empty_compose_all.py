
def test_empty_compose_all():
    with pytest.raises(ValueError):
        nx.compose_all([])

