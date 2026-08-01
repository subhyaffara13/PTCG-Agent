
def test_hilbert():
    h1 = HilbertSpace()
    h2 = ComplexSpace(2)
    h3 = FockSpace()
    h4 = L2(Interval(0, oo))
    assert str(h1) == 'H'
    assert pretty(h1) == 'H'
    assert upretty(h1) == 'H'
    assert latex(h1) == r'\mathcal{H}'
    sT(h1, "HilbertSpace()")
    assert str(h2) == 'C(2)'
    ascii_str = \
"""\
 2\n\
C \
"""
    ucode_str = \
"""\
 2\n\
C \
"""
    assert pretty(h2) == ascii_str
    assert upretty(h2) == ucode_str
    assert latex(h2) == r'\mathcal{C}^{2}'
    sT(h2, "ComplexSpace(Integer(2))")
    assert str(h3) == 'F'
    assert pretty(h3) == 'F'
    assert upretty(h3) == 'F'
    assert latex(h3) == r'\mathcal{F}'
    sT(h3, "FockSpace()")
    assert str(h4) == 'L2(Interval(0, oo))'
    ascii_str = \
"""\
 2\n\
L \
"""
    ucode_str = \
"""\
 2\n\
L \
"""
    assert pretty(h4) == ascii_str
    assert upretty(h4) == ucode_str
    assert latex(h4) == r'{\mathcal{L}^2}\left( \left[0, \infty\right) \right)'
    sT(h4, "L2(Interval(Integer(0), oo, false, true))")
    assert str(h1 + h2) == 'H+C(2)'
    ascii_str = \
"""\
     2\n\
H + C \
"""
    ucode_str = \
"""\
     2\n\
H ⊕ C \
"""
    assert pretty(h1 + h2) == ascii_str
    assert upretty(h1 + h2) == ucode_str
    assert latex(h1 + h2)
    sT(h1 + h2, "DirectSumHilbertSpace(HilbertSpace(),ComplexSpace(Integer(2)))")
    assert str(h1*h2) == "H*C(2)"
    ascii_str = \
"""\
     2\n\
H x C \
"""
    ucode_str = \
"""\
     2\n\
H ⨂ C \
"""
    assert pretty(h1*h2) == ascii_str
    assert upretty(h1*h2) == ucode_str
    assert latex(h1*h2)
    sT(h1*h2,
       "TensorProductHilbertSpace(HilbertSpace(),ComplexSpace(Integer(2)))")
    assert str(h1**2) == 'H**2'
    ascii_str = \
"""\
 x2\n\
H  \
"""
    ucode_str = \
"""\
 ⨂2\n\
H  \
"""
    assert pretty(h1**2) == ascii_str
    assert upretty(h1**2) == ucode_str
    assert latex(h1**2) == r'{\mathcal{H}}^{\otimes 2}'
    sT(h1**2, "TensorPowerHilbertSpace(HilbertSpace(),Integer(2))")

