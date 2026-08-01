
def test_non_mutable_get_values(kind):
    cmap = copy.copy(mpl.colormaps['viridis'])
    init_value = getattr(cmap, f'get_{kind}')()
    with pytest.warns(PendingDeprecationWarning):
        getattr(cmap, f'set_{kind}')('k')
    black_value = getattr(cmap, f'get_{kind}')()
    assert np.all(black_value == [0, 0, 0, 1])
    assert not np.all(init_value == black_value)

