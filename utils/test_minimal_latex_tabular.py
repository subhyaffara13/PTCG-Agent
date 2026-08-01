
def test_minimal_latex_tabular(styler):
    expected = dedent(
        """\
        \\begin{tabular}{lrrl}
         & A & B & C \\\\
        0 & 0 & -0.61 & ab \\\\
        1 & 1 & -1.22 & cd \\\\
        \\end{tabular}
        """
    )
    assert styler.to_latex() == expected

