
def test_operators_notimplemented():
    """#393: need to return NotSupported to ensure correct arithmetic operator behavior"""

    c1, c2 = m.C1(), m.C2()
    assert c1 + c1 == 11
    assert c2 + c2 == 22
    assert c2 + c1 == 21
    assert c1 + c2 == 12

