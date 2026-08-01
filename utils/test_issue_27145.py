
def test_issue_27145():
    #https://github.com/sympy/sympy/issues/27145
    assert [mr(i,[2,3,5,7]) for i in (1, 2, 6)] == [False, True, False]

