
def test_dispatch_issue(msg):
    """#159: virtual function dispatch has problems with similar-named functions"""

    class PyClass1(m.DispatchIssue):
        def dispatch(self):
            return "Yay.."

    class PyClass2(m.DispatchIssue):
        def dispatch(self):
            with pytest.raises(RuntimeError) as excinfo:
                super().dispatch()
            assert (
                msg(excinfo.value)
                == 'Tried to call pure virtual function "Base::dispatch"'
            )

            return m.dispatch_issue_go(PyClass1())

    b = PyClass2()
    assert m.dispatch_issue_go(b) == "Yay.."

