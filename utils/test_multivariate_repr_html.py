
def test_multivariate_repr_html():
    cmap = mpl.multivar_colormaps['3VarAddA']
    html = cmap._repr_html_()
    assert len(html) > 0
    for c in cmap:
        png = c._repr_png_()
        assert base64.b64encode(png).decode('ascii') in html
    assert cmap.name in html
    assert html.startswith('<div')
    assert html.endswith('</div>')

