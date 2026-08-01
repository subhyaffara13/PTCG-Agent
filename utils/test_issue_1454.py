
def test_issue_1454():
    # Fix issue #1454 (crash when acquiring/releasing GIL on another thread in Python 2.7)
    m.test_gil()
    m.test_gil_from_thread()

