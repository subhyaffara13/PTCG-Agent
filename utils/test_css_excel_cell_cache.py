
def test_css_excel_cell_cache(styles, cache_hits, cache_misses):
    """It caches unique cell styles"""
    # See GH 47371
    converter = CSSToExcelConverter()
    converter._call_cached.cache_clear()

    css_styles = {(0, i): _style for i, _style in enumerate(styles)}
    for css_row, css_col in css_styles:
        CssExcelCell(
            row=0,
            col=0,
            val="",
            style=None,
            css_styles=css_styles,
            css_row=css_row,
            css_col=css_col,
            css_converter=converter,
        )
    cache_info = converter._call_cached.cache_info()
    converter._call_cached.cache_clear()

    assert cache_info.hits == cache_hits
    assert cache_info.misses == cache_misses

