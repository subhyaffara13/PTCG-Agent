
def test_latex_mul_symbol():
    assert latex(4*4**x, mul_symbol='times') == r"4 \times 4^{x}"
    assert latex(4*4**x, mul_symbol='dot') == r"4 \cdot 4^{x}"
    assert latex(4*4**x, mul_symbol='ldot') == r"4 \,.\, 4^{x}"

    assert latex(4*x, mul_symbol='times') == r"4 \times x"
    assert latex(4*x, mul_symbol='dot') == r"4 \cdot x"
    assert latex(4*x, mul_symbol='ldot') == r"4 \,.\, x"

