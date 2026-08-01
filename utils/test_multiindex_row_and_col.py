
def test_multiindex_row_and_col(df_ext):
    cidx = MultiIndex.from_tuples([("Z", "a"), ("Z", "b"), ("Y", "c")])
    ridx = MultiIndex.from_tuples([("A", "a"), ("A", "b"), ("B", "c")])
    df_ext.index, df_ext.columns = ridx, cidx
    expected = dedent(
        """\
        \\begin{tabular}{llrrl}
         &  & \\multicolumn{2}{l}{Z} & Y \\\\
         &  & a & b & c \\\\
        \\multirow[b]{2}{*}{A} & a & 0 & -0.61 & ab \\\\
         & b & 1 & -1.22 & cd \\\\
        B & c & 2 & -2.22 & de \\\\
        \\end{tabular}
        """
    )
    styler = df_ext.style.format(precision=2)
    result = styler.to_latex(multirow_align="b", multicol_align="l")
    assert result == expected

    # non-sparse
    expected = dedent(
        """\
        \\begin{tabular}{llrrl}
         &  & Z & Z & Y \\\\
         &  & a & b & c \\\\
        A & a & 0 & -0.61 & ab \\\\
        A & b & 1 & -1.22 & cd \\\\
        B & c & 2 & -2.22 & de \\\\
        \\end{tabular}
        """
    )
    result = styler.to_latex(sparse_index=False, sparse_columns=False)
    assert result == expected

