
def test_Module_NotImplemented():
    M = Module()
    raises(NotImplementedError, lambda: M.n)
    raises(NotImplementedError, lambda: M.mult_tab())
    raises(NotImplementedError, lambda: M.represent(None))
    raises(NotImplementedError, lambda: M.starts_with_unity())
    raises(NotImplementedError, lambda: M.element_from_rational(QQ(2, 3)))

