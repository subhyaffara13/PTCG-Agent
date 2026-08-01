
def test_tab_complete_ipython6_warning(ip):
    from IPython.core.completer import provisionalcompleter

    code = dedent(
        """\
    import numpy as np
    from pandas import Series, date_range
    data = np.arange(10, dtype=np.float64)
    index = date_range("2020-01-01", periods=len(data))
    s = Series(data, index=index)
    rs = s.resample("D")
    """
    )
    ip.run_cell(code)

    # GH 31324 newer jedi version raises Deprecation warning;
    #  appears resolved 2021-02-02
    with tm.assert_produces_warning(None, raise_on_extra_warnings=False):
        with provisionalcompleter("ignore"):
            list(ip.Completer.completions("rs.", 1))

