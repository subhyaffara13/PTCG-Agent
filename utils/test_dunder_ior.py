
def test_dunder_ior(d, Asp):
    if isinstance(Asp, dok_array):
        with pytest.raises(TypeError):
            Asp |= Asp
    else:
        dd = {(0, 0): 5}
        Asp |= dd
        assert Asp[(0, 0)] == 5
        d |= dd
        assert d.items() == Asp.items()
        dd |= Asp
        assert dd.items() == Asp.items()

