
def test_NumPyPrinter_print_seq():
    n = NumPyPrinter()

    assert n._print_seq(range(2)) == '(0, 1,)'

