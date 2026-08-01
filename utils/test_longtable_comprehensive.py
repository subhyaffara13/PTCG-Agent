
def test_longtable_comprehensive(styler):
    result = styler.to_latex(
        environment="longtable", hrules=True, label="fig:A", caption=("full", "short")
    )
    expected = dedent(
        """\
        \\begin{longtable}{lrrl}
        \\caption[short]{full} \\label{fig:A} \\\\
        \\toprule
         & A & B & C \\\\
        \\midrule
        \\endfirsthead
        \\caption[]{full} \\\\
        \\toprule
         & A & B & C \\\\
        \\midrule
        \\endhead
        \\midrule
        \\multicolumn{4}{r}{Continued on next page} \\\\
        \\midrule
        \\endfoot
        \\bottomrule
        \\endlastfoot
        0 & 0 & -0.61 & ab \\\\
        1 & 1 & -1.22 & cd \\\\
        \\end{longtable}
    """
    )
    assert result == expected

