
def test_exception_rvalue_abort():
    with pytest.raises(RuntimeError):
        m.PyPrintDestructor().throw_something()

