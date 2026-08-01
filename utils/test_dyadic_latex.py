
def test_dyadic_latex():

    expected = (r'a^{2}\mathbf{\hat{n}_x}\otimes \mathbf{\hat{n}_y} + '
                r'b\mathbf{\hat{n}_y}\otimes \mathbf{\hat{n}_y} + '
                r'c \sin{\left(\alpha \right)}'
                r'\mathbf{\hat{n}_z}\otimes \mathbf{\hat{n}_y}')

    assert vlatex(y) == expected

    expected = (r'\alpha\mathbf{\hat{n}_x}\otimes \mathbf{\hat{n}_x} + '
                r'\sin{\left(\omega \right)}\mathbf{\hat{n}_y}'
                r'\otimes \mathbf{\hat{n}_z} + '
                r'\alpha \beta\mathbf{\hat{n}_z}\otimes \mathbf{\hat{n}_x}')

    assert vlatex(x) == expected

    assert vlatex(Dyadic([])) == '0'

