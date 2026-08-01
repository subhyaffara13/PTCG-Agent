
def test_dunder_reversed(d, Asp):
    if isinstance(Asp, dok_array):
        with pytest.raises(TypeError):
            list(reversed(Asp))
    else:
        assert list(reversed(Asp)) == list(reversed(d))

