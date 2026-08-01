
def test_clear(d, Asp):
    assert d.items() == Asp.items()
    d.clear()
    Asp.clear()
    assert d.items() == Asp.items()


def test_clear(mi_styler_comp):
    # NOTE: if this test fails for new features then 'mi_styler_comp' should be updated
    # to ensure proper testing of the 'copy', 'clear', 'export' methods with new feature
    # GH 40675
    styler = mi_styler_comp
    styler._compute()  # execute applied methods

    clean_copy = Styler(styler.data, uuid=styler.uuid)

    excl = [
        "data",
        "index",
        "columns",
        "uuid",
        "uuid_len",  # uuid is set to be the same on styler and clean_copy
        "cell_ids",
        "cellstyle_map",  # execution time only
        "cellstyle_map_columns",  # execution time only
        "cellstyle_map_index",  # execution time only
        "template_latex",  # render templates are class level
        "template_html",
        "template_html_style",
        "template_html_table",
    ]
    # tests vars are not same vals on obj and clean copy before clear (except for excl)
    for attr in [a for a in styler.__dict__ if not (callable(a) or a in excl)]:
        res = getattr(styler, attr) == getattr(clean_copy, attr)
        if hasattr(res, "__iter__") and len(res) > 0:
            assert not all(res)  # some element in iterable differs
        elif hasattr(res, "__iter__") and len(res) == 0:
            pass  # empty array
        else:
            assert not res  # explicit var differs

    # test vars have same vales on obj and clean copy after clearing
    styler.clear()
    for attr in [a for a in styler.__dict__ if not callable(a)]:
        res = getattr(styler, attr) == getattr(clean_copy, attr)
        assert all(res) if hasattr(res, "__iter__") else res

