
def test_unit_printing():
    assert latex(5*meter) == r'5 \text{m}'
    assert latex(3*gibibyte) == r'3 \text{gibibyte}'
    assert latex(4*microgram/second) == r'\frac{4 \mu\text{g}}{\text{s}}'
    assert latex(4*micro*gram/second) == r'\frac{4 \mu \text{g}}{\text{s}}'
    assert latex(5*milli*meter) == r'5 \text{m} \text{m}'
    assert latex(milli) == r'\text{m}'

