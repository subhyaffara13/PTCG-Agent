
def test_fontentry_dataclass():
    fontent = FontEntry(name='font-name')

    png = fontent._repr_png_()
    img = Image.open(BytesIO(png))
    assert img.width > 0
    assert img.height > 0

    html = fontent._repr_html_()
    assert html.startswith("<img src=\"data:image/png;base64")

