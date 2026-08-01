
def test_dunder_ror(d, Asp):
    if isinstance(Asp, dok_array):
        with pytest.raises(TypeError):
            Asp | Asp
        with pytest.raises(TypeError):
            d | Asp
    else:
        assert Asp.__ror__(d) == Asp.__ror__(Asp)
        assert d.__ror__(d) == Asp.__ror__(d)
        assert d | Asp

