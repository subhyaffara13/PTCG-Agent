
def test_bug_17380():
    linprog([1, 1], A_ub=[[-1, 0]], b_ub=[-2.5], integrality=[1, 1])

