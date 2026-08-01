
def test_mi_styler_sparsify_options(mi_styler):
    with option_context("styler.sparse.index", False):
        html1 = mi_styler.to_html()
    with option_context("styler.sparse.index", True):
        html2 = mi_styler.to_html()

    assert html1 != html2

    with option_context("styler.sparse.columns", False):
        html1 = mi_styler.to_html()
    with option_context("styler.sparse.columns", True):
        html2 = mi_styler.to_html()

    assert html1 != html2

