
def test_issue_16859():
    class no(float, CantSympify):
        pass
    raises(SympifyError, lambda: sympify(no(1.2)))

