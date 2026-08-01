
def test_bivariate_repr_html():
    cmap = mpl.bivar_colormaps['BiCone']
    html = cmap._repr_html_()
    assert len(html) > 0
    png = cmap._repr_png_()
    assert base64.b64encode(png).decode('ascii') in html
    assert cmap.name in html
    assert html.startswith('<div')
    assert html.endswith('</div>')

