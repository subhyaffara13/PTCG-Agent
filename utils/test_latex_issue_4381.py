
def test_latex_issue_4381():
    y = 4*4**log(2)
    assert latex(y) == r'4 \cdot 4^{\log{\left(2 \right)}}'
    assert latex(1/y) == r'\frac{1}{4 \cdot 4^{\log{\left(2 \right)}}}'

