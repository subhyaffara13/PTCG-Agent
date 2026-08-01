
def test_multicol_naive(df, multicol_align, siunitx, header):
    ridx = MultiIndex.from_tuples([("A", "a"), ("A", "b"), ("A", "c")])
    df.columns = ridx
    level1 = " & a & b & c" if not siunitx else "{} & {a} & {b} & {c}"
    col_format = "lrrl" if not siunitx else "lSSl"
    expected = dedent(
        f"""\
        \\begin{{tabular}}{{{col_format}}}
        {header} \\\\
        {level1} \\\\
        0 & 0 & -0.61 & ab \\\\
        1 & 1 & -1.22 & cd \\\\
        \\end{{tabular}}
        """
    )
    styler = df.style.format(precision=2)
    result = styler.to_latex(multicol_align=multicol_align, siunitx=siunitx)
    assert expected == result

