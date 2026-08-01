
def test_vector_latex_arguments():
    assert vlatex(N.x * 3.0, full_prec=False) == r'3.0\mathbf{\hat{n}_x}'
    assert vlatex(N.x * 3.0, full_prec=True) == r'3.00000000000000\mathbf{\hat{n}_x}'

