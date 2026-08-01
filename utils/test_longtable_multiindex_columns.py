
def test_longtable_multiindex_columns(df, sparse, exp, siunitx):
    cidx = MultiIndex.from_tuples([("A", "a"), ("A", "b"), ("B", "c")])
    df.columns = cidx
    with_si = "{} & {a} & {b} & {c} \\\\"
    without_si = " & a & b & c \\\\"
    expected = dedent(
        f"""\
        \\begin{{longtable}}{{l{"SS" if siunitx else "rr"}l}}
        {exp} \\\\
        {with_si if siunitx else without_si}
        \\endfirsthead
        {exp} \\\\
        {with_si if siunitx else without_si}
        \\endhead
        """
    )
    result = df.style.to_latex(
        environment="longtable", sparse_columns=sparse, siunitx=siunitx
    )
    assert expected in result

