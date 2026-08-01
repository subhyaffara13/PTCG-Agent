
def test_issue_21245():
    fi = (1 + sqrt(5))/2
    assert (1/(1 - x - x**2)).series(x, 1/fi, 1).factor() == \
        (-37*sqrt(5) - 83 + 13*sqrt(5)*x + 29*x + O((x - 2/(1 + sqrt(5)))**2, (x\
            , 2/(1 + sqrt(5)))))/((2*sqrt(5) + 5)**2*(x + sqrt(5)*x - 2))

