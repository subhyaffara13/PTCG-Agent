
def test_comprehensive(df_ext, environment):
    # test as many low level features simultaneously as possible
    cidx = MultiIndex.from_tuples([("Z", "a"), ("Z", "b"), ("Y", "c")])
    ridx = MultiIndex.from_tuples([("A", "a"), ("A", "b"), ("B", "c")])
    df_ext.index, df_ext.columns = ridx, cidx
    stlr = df_ext.style
    stlr.set_caption("mycap")
    stlr.set_table_styles(
        [
            {"selector": "label", "props": ":{fig§item}"},
            {"selector": "position", "props": ":h!"},
            {"selector": "position_float", "props": ":centering"},
            {"selector": "column_format", "props": ":rlrlr"},
            {"selector": "toprule", "props": ":toprule"},
            {"selector": "midrule", "props": ":midrule"},
            {"selector": "bottomrule", "props": ":bottomrule"},
            {"selector": "rowcolors", "props": ":{3}{pink}{}"},  # custom command
        ]
    )
    stlr.highlight_max(axis=0, props="textbf:--rwrap;cellcolor:[rgb]{1,1,0.6}--rwrap")
    stlr.highlight_max(axis=None, props="Huge:--wrap;", subset=[("Z", "a"), ("Z", "b")])

    expected = (
        """\
\\begin{table}[h!]
\\centering
\\caption{mycap}
\\label{fig:item}
\\rowcolors{3}{pink}{}
\\begin{tabular}{rlrlr}
\\toprule
 &  & \\multicolumn{2}{r}{Z} & Y \\\\
 &  & a & b & c \\\\
\\midrule
\\multirow[c]{2}{*}{A} & a & 0 & \\textbf{\\cellcolor[rgb]{1,1,0.6}{-0.61}} & ab \\\\
 & b & 1 & -1.22 & cd \\\\
B & c & \\textbf{\\cellcolor[rgb]{1,1,0.6}{{\\Huge 2}}} & -2.22 & """
        """\
\\textbf{\\cellcolor[rgb]{1,1,0.6}{de}} \\\\
\\bottomrule
\\end{tabular}
\\end{table}
"""
    ).replace("table", environment if environment else "table")
    result = stlr.format(precision=2).to_latex(environment=environment)
    assert result == expected

