
def test_apply_map_header_render_mi(df_ext, index, columns, siunitx):
    cidx = MultiIndex.from_tuples([("Z", "a"), ("Z", "b"), ("Y", "c")])
    ridx = MultiIndex.from_tuples([("A", "a"), ("A", "b"), ("B", "c")])
    df_ext.index, df_ext.columns = ridx, cidx
    styler = df_ext.style

    func = lambda v: "bfseries: --rwrap" if "A" in v or "Z" in v or "c" in v else None

    if index:
        styler.map_index(func, axis="index")
    if columns:
        styler.map_index(func, axis="columns")

    result = styler.to_latex(siunitx=siunitx)

    expected_index = dedent(
        """\
    \\multirow[c]{2}{*}{\\bfseries{A}} & a & 0 & -0.610000 & ab \\\\
    \\bfseries{} & b & 1 & -1.220000 & cd \\\\
    B & \\bfseries{c} & 2 & -2.220000 & de \\\\
    """
    )
    assert (expected_index in result) is index

    exp_cols_si = dedent(
        """\
    {} & {} & \\multicolumn{2}{r}{\\bfseries{Z}} & {Y} \\\\
    {} & {} & {a} & {b} & {\\bfseries{c}} \\\\
    """
    )
    exp_cols_no_si = """\
 &  & \\multicolumn{2}{r}{\\bfseries{Z}} & Y \\\\
 &  & a & b & \\bfseries{c} \\\\
"""
    assert ((exp_cols_si if siunitx else exp_cols_no_si) in result) is columns

