
def test_multiline_latex():
    a, b, c, d, e, f = symbols('a b c d e f')
    expr = -a + 2*b -3*c +4*d -5*e
    expected = r"\begin{eqnarray}" + "\n"\
        r"f & = &- a \nonumber\\" + "\n"\
        r"& & + 2 b \nonumber\\" + "\n"\
        r"& & - 3 c \nonumber\\" + "\n"\
        r"& & + 4 d \nonumber\\" + "\n"\
        r"& & - 5 e " + "\n"\
        r"\end{eqnarray}"
    assert multiline_latex(f, expr, environment="eqnarray") == expected

    expected2 = r'\begin{eqnarray}' + '\n'\
        r'f & = &- a + 2 b \nonumber\\' + '\n'\
        r'& & - 3 c + 4 d \nonumber\\' + '\n'\
        r'& & - 5 e ' + '\n'\
        r'\end{eqnarray}'

    assert multiline_latex(f, expr, 2, environment="eqnarray") == expected2

    expected3 = r'\begin{eqnarray}' + '\n'\
        r'f & = &- a + 2 b - 3 c \nonumber\\'+ '\n'\
        r'& & + 4 d - 5 e ' + '\n'\
        r'\end{eqnarray}'

    assert multiline_latex(f, expr, 3, environment="eqnarray") == expected3

    expected3dots = r'\begin{eqnarray}' + '\n'\
        r'f & = &- a + 2 b - 3 c \dots\nonumber\\'+ '\n'\
        r'& & + 4 d - 5 e ' + '\n'\
        r'\end{eqnarray}'

    assert multiline_latex(f, expr, 3, environment="eqnarray", use_dots=True) == expected3dots

    expected3align = r'\begin{align*}' + '\n'\
        r'f = &- a + 2 b - 3 c \\'+ '\n'\
        r'& + 4 d - 5 e ' + '\n'\
        r'\end{align*}'

    assert multiline_latex(f, expr, 3) == expected3align
    assert multiline_latex(f, expr, 3, environment='align*') == expected3align

    expected2ieee = r'\begin{IEEEeqnarray}{rCl}' + '\n'\
        r'f & = &- a + 2 b \nonumber\\' + '\n'\
        r'& & - 3 c + 4 d \nonumber\\' + '\n'\
        r'& & - 5 e ' + '\n'\
        r'\end{IEEEeqnarray}'

    assert multiline_latex(f, expr, 2, environment="IEEEeqnarray") == expected2ieee

    raises(ValueError, lambda: multiline_latex(f, expr, environment="foo"))

