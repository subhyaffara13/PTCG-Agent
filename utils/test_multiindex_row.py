
def test_multiindex_row(df_ext):
    ridx = MultiIndex.from_tuples([("A", "a"), ("A", "b"), ("B", "c")])
    df_ext.index = ridx
    expected = dedent(
        """\
        \\begin{tabular}{llrrl}
         &  & A & B & C \\\\
        \\multirow[c]{2}{*}{A} & a & 0 & -0.61 & ab \\\\
         & b & 1 & -1.22 & cd \\\\
        B & c & 2 & -2.22 & de \\\\
        \\end{tabular}
        """
    )
    styler = df_ext.style.format(precision=2)
    result = styler.to_latex()
    assert expected == result

    # non-sparse
    expected = dedent(
        """\
        \\begin{tabular}{llrrl}
         &  & A & B & C \\\\
        A & a & 0 & -0.61 & ab \\\\
        A & b & 1 & -1.22 & cd \\\\
        B & c & 2 & -2.22 & de \\\\
        \\end{tabular}
        """
    )
    result = styler.to_latex(sparse_index=False)
    assert expected == result

