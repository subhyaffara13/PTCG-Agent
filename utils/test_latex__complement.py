
def test_latex_Complement():
    assert latex(Complement(S.Reals, S.Naturals)) == \
        r"\mathbb{R} \setminus \mathbb{N}"

