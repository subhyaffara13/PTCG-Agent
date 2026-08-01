
def test_content_mathml_matrices():
    A = Matrix([1, 2, 3])
    B = Matrix([[0, 5, 4], [2, 3, 1], [9, 7, 9]])
    mll_1 = mp._print(A)
    assert mll_1.childNodes[0].nodeName == 'matrixrow'
    assert mll_1.childNodes[0].childNodes[0].nodeName == 'cn'
    assert mll_1.childNodes[0].childNodes[0].childNodes[0].nodeValue == '1'
    assert mll_1.childNodes[1].nodeName == 'matrixrow'
    assert mll_1.childNodes[1].childNodes[0].nodeName == 'cn'
    assert mll_1.childNodes[1].childNodes[0].childNodes[0].nodeValue == '2'
    assert mll_1.childNodes[2].nodeName == 'matrixrow'
    assert mll_1.childNodes[2].childNodes[0].nodeName == 'cn'
    assert mll_1.childNodes[2].childNodes[0].childNodes[0].nodeValue == '3'
    mll_2 = mp._print(B)
    assert mll_2.childNodes[0].nodeName == 'matrixrow'
    assert mll_2.childNodes[0].childNodes[0].nodeName == 'cn'
    assert mll_2.childNodes[0].childNodes[0].childNodes[0].nodeValue == '0'
    assert mll_2.childNodes[0].childNodes[1].nodeName == 'cn'
    assert mll_2.childNodes[0].childNodes[1].childNodes[0].nodeValue == '5'
    assert mll_2.childNodes[0].childNodes[2].nodeName == 'cn'
    assert mll_2.childNodes[0].childNodes[2].childNodes[0].nodeValue == '4'
    assert mll_2.childNodes[1].nodeName == 'matrixrow'
    assert mll_2.childNodes[1].childNodes[0].nodeName == 'cn'
    assert mll_2.childNodes[1].childNodes[0].childNodes[0].nodeValue == '2'
    assert mll_2.childNodes[1].childNodes[1].nodeName == 'cn'
    assert mll_2.childNodes[1].childNodes[1].childNodes[0].nodeValue == '3'
    assert mll_2.childNodes[1].childNodes[2].nodeName == 'cn'
    assert mll_2.childNodes[1].childNodes[2].childNodes[0].nodeValue == '1'
    assert mll_2.childNodes[2].nodeName == 'matrixrow'
    assert mll_2.childNodes[2].childNodes[0].nodeName == 'cn'
    assert mll_2.childNodes[2].childNodes[0].childNodes[0].nodeValue == '9'
    assert mll_2.childNodes[2].childNodes[1].nodeName == 'cn'
    assert mll_2.childNodes[2].childNodes[1].childNodes[0].nodeValue == '7'
    assert mll_2.childNodes[2].childNodes[2].nodeName == 'cn'
    assert mll_2.childNodes[2].childNodes[2].childNodes[0].nodeValue == '9'

