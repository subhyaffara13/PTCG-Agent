
def test_nat_methods_nat(method):
    # see gh-8254, gh-9513, gh-17329
    assert getattr(NaT, method)() is NaT

