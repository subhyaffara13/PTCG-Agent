
def test_update(d, Asp):
    for input in [Asp, Asp._dict, Asp._dict.items()]:
        Bsp = dok_array(Asp.shape)
        Bsp.update(input)
        assert_equal(Bsp.toarray(), Asp.toarray())

    with pytest.raises(ValueError, match="Inexact indices .* not allowed"):
        Asp.update(np.zeros((2,2)))
    with pytest.raises(IndexError, match="length needs to match self.shape"):
        Asp.update({(3, 2, 1, 0): 1.2})
    with pytest.raises(IndexError, match="integer keys required"):
        Asp.update({(0.2, 1): 1.2})
    with pytest.raises(IndexError, match="negative index"):
        Asp.update({(0, -1): 1.2})
    with pytest.raises(IndexError, match="index .* is too large"):
        Asp.update({(0, 3): 1.2})


def test_update():
    gs = gridspec.GridSpec(2, 1)

    gs.update(left=.1)
    assert gs.left == .1

