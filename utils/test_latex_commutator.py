
def test_latex_commutator():
    A = Operator('A')
    B = Operator('B')
    comm = Commutator(B, A)
    assert latex(comm.doit()) == r"- (A B - B A)"

