
def test_issue_18842():
    f = log(x/(1 - x))
    assert f.series(x, 0.491, n=1).removeO().nsimplify() ==  \
        -S(180019443780011)/5000000000000000

