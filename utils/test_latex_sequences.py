
def test_latex_sequences():
    s1 = SeqFormula(a**2, (0, oo))
    s2 = SeqPer((1, 2))

    latex_str = r'\left[0, 1, 4, 9, \ldots\right]'
    assert latex(s1) == latex_str

    latex_str = r'\left[1, 2, 1, 2, \ldots\right]'
    assert latex(s2) == latex_str

    s3 = SeqFormula(a**2, (0, 2))
    s4 = SeqPer((1, 2), (0, 2))

    latex_str = r'\left[0, 1, 4\right]'
    assert latex(s3) == latex_str

    latex_str = r'\left[1, 2, 1\right]'
    assert latex(s4) == latex_str

    s5 = SeqFormula(a**2, (-oo, 0))
    s6 = SeqPer((1, 2), (-oo, 0))

    latex_str = r'\left[\ldots, 9, 4, 1, 0\right]'
    assert latex(s5) == latex_str

    latex_str = r'\left[\ldots, 2, 1, 2, 1\right]'
    assert latex(s6) == latex_str

    latex_str = r'\left[1, 3, 5, 11, \ldots\right]'
    assert latex(SeqAdd(s1, s2)) == latex_str

    latex_str = r'\left[1, 3, 5\right]'
    assert latex(SeqAdd(s3, s4)) == latex_str

    latex_str = r'\left[\ldots, 11, 5, 3, 1\right]'
    assert latex(SeqAdd(s5, s6)) == latex_str

    latex_str = r'\left[0, 2, 4, 18, \ldots\right]'
    assert latex(SeqMul(s1, s2)) == latex_str

    latex_str = r'\left[0, 2, 4\right]'
    assert latex(SeqMul(s3, s4)) == latex_str

    latex_str = r'\left[\ldots, 18, 4, 2, 0\right]'
    assert latex(SeqMul(s5, s6)) == latex_str

    # Sequences with symbolic limits, issue 12629
    s7 = SeqFormula(a**2, (a, 0, x))
    latex_str = r'\left\{a^{2}\right\}_{a=0}^{x}'
    assert latex(s7) == latex_str

    b = Symbol('b')
    s8 = SeqFormula(b*a**2, (a, 0, 2))
    latex_str = r'\left[0, b, 4 b\right]'
    assert latex(s8) == latex_str

