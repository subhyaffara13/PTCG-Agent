
def test_dunder_or(d, Asp):
    if isinstance(Asp, dok_array):
        with pytest.raises(TypeError):
            Asp | Asp
    else:
        assert d | d == Asp | d
        assert d | d == Asp | Asp

