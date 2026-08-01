
def test_hidden_index(styler):
    styler.hide(axis="index")
    expected = dedent(
        """\
        \\begin{tabular}{rrl}
        A & B & C \\\\
        0 & -0.61 & ab \\\\
        1 & -1.22 & cd \\\\
        \\end{tabular}
        """
    )
    assert styler.to_latex() == expected

