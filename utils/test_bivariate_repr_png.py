
def test_bivariate_repr_png():
    cmap = mpl.bivar_colormaps['BiCone']
    png = cmap._repr_png_()
    assert len(png) > 0
    img = Image.open(BytesIO(png))
    assert img.width > 0
    assert img.height > 0
    assert 'Title' in img.text
    assert 'Description' in img.text
    assert 'Author' in img.text
    assert 'Software' in img.text

