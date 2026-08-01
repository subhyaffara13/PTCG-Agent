
def test_cg():
    cg = CG(1, 2, 3, 4, 5, 6)
    wigner3j = Wigner3j(1, 2, 3, 4, 5, 6)
    wigner6j = Wigner6j(1, 2, 3, 4, 5, 6)
    wigner9j = Wigner9j(1, 2, 3, 4, 5, 6, 7, 8, 9)
    assert str(cg) == 'CG(1, 2, 3, 4, 5, 6)'
    ascii_str = \
"""\
 5,6    \n\
C       \n\
 1,2,3,4\
"""
    ucode_str = \
"""\
 5,6    \n\
C       \n\
 1,2,3,4\
"""
    assert pretty(cg) == ascii_str
    assert upretty(cg) == ucode_str
    assert latex(cg) == 'C^{5,6}_{1,2,3,4}'
    assert latex(cg ** 2) == R'\left(C^{5,6}_{1,2,3,4}\right)^{2}'
    sT(cg, "CG(Integer(1), Integer(2), Integer(3), Integer(4), Integer(5), Integer(6))")
    assert str(wigner3j) == 'Wigner3j(1, 2, 3, 4, 5, 6)'
    ascii_str = \
"""\
/1  3  5\\\n\
|       |\n\
\\2  4  6/\
"""
    ucode_str = \
"""\
⎛1  3  5⎞\n\
⎜       ⎟\n\
⎝2  4  6⎠\
"""
    assert pretty(wigner3j) == ascii_str
    assert upretty(wigner3j) == ucode_str
    assert latex(wigner3j) == \
        r'\left(\begin{array}{ccc} 1 & 3 & 5 \\ 2 & 4 & 6 \end{array}\right)'
    sT(wigner3j, "Wigner3j(Integer(1), Integer(2), Integer(3), Integer(4), Integer(5), Integer(6))")
    assert str(wigner6j) == 'Wigner6j(1, 2, 3, 4, 5, 6)'
    ascii_str = \
"""\
/1  2  3\\\n\
<       >\n\
\\4  5  6/\
"""
    ucode_str = \
"""\
⎧1  2  3⎫\n\
⎨       ⎬\n\
⎩4  5  6⎭\
"""
    assert pretty(wigner6j) == ascii_str
    assert upretty(wigner6j) == ucode_str
    assert latex(wigner6j) == \
        r'\left\{\begin{array}{ccc} 1 & 2 & 3 \\ 4 & 5 & 6 \end{array}\right\}'
    sT(wigner6j, "Wigner6j(Integer(1), Integer(2), Integer(3), Integer(4), Integer(5), Integer(6))")
    assert str(wigner9j) == 'Wigner9j(1, 2, 3, 4, 5, 6, 7, 8, 9)'
    ascii_str = \
"""\
/1  2  3\\\n\
|       |\n\
<4  5  6>\n\
|       |\n\
\\7  8  9/\
"""
    ucode_str = \
"""\
⎧1  2  3⎫\n\
⎪       ⎪\n\
⎨4  5  6⎬\n\
⎪       ⎪\n\
⎩7  8  9⎭\
"""
    assert pretty(wigner9j) == ascii_str
    assert upretty(wigner9j) == ucode_str
    assert latex(wigner9j) == \
        r'\left\{\begin{array}{ccc} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{array}\right\}'
    sT(wigner9j, "Wigner9j(Integer(1), Integer(2), Integer(3), Integer(4), Integer(5), Integer(6), Integer(7), Integer(8), Integer(9))")

