
def test_invalid_name():
    with pytest.raises(ValueError):
        triad_graph("bogus")

