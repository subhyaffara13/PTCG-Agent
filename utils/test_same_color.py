
def test_same_color():
    assert mcolors.same_color('k', (0, 0, 0))
    assert not mcolors.same_color('w', (1, 1, 0))
    assert mcolors.same_color(['red', 'blue'], ['r', 'b'])
    assert mcolors.same_color('none', 'none')
    assert not mcolors.same_color('none', 'red')
    with pytest.raises(ValueError):
        mcolors.same_color(['r', 'g', 'b'], ['r'])
    with pytest.raises(ValueError):
        mcolors.same_color(['red', 'green'], 'none')

