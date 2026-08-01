
def test_issue_9539():
    assert diophantine(6*w + 9*y + 20*x - z) == \
           {(t_0, t_1, t_1 + t_2, 6*t_0 + 29*t_1 + 9*t_2)}

