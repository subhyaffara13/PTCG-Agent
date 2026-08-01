
def test_invalid_args():
    raises(SympifyError, lambda: MatrixSymbol(1, 2, 'A'))

