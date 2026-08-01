
def test_apply_index_hidden_levels():
    # gh 45156
    styler = DataFrame(
        [[1]],
        index=MultiIndex.from_tuples([(0, 1)], names=["l0", "l1"]),
        columns=MultiIndex.from_tuples([(0, 1)], names=["c0", "c1"]),
    ).style
    styler.hide(level=1)
    styler.map_index(lambda v: "color: red;", level=0, axis=1)
    result = styler.to_latex(convert_css=True)
    expected = dedent(
        """\
        \\begin{tabular}{lr}
        c0 & \\color{red} 0 \\\\
        c1 & 1 \\\\
        l0 &  \\\\
        0 & 1 \\\\
        \\end{tabular}
        """
    )
    assert result == expected

