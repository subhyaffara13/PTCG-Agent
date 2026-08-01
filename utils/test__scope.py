
def test_Scope():
    assign = Assignment(x, y)
    incr = AddAugmentedAssignment(x, 1)
    scp = Scope([assign, incr])
    cblk = CodeBlock(assign, incr)
    assert scp.body == cblk
    assert scp == Scope(cblk)
    assert scp != Scope([incr, assign])
    assert scp.func(*scp.args) == scp

