
def test_multivar_bad_mode():
    cmap = mpl.multivar_colormaps['2VarSubA']
    with pytest.raises(ValueError, match="is not a valid value for"):
        cmap = mpl.colors.MultivarColormap(cmap[:], 'bad')

