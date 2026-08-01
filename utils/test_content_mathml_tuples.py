
def test_content_mathml_tuples():
    mml_1 = mp._print([2])
    assert mml_1.nodeName == 'list'
    assert mml_1.childNodes[0].nodeName == 'cn'
    assert len(mml_1.childNodes) == 1

    mml_2 = mp._print([2, Integer(1)])
    assert mml_2.nodeName == 'list'
    assert mml_2.childNodes[0].nodeName == 'cn'
    assert mml_2.childNodes[1].nodeName == 'cn'
    assert len(mml_2.childNodes) == 2

