
def test_issue_2460():
    bdm1 = BlockDiagMatrix(Matrix([i]), Matrix([j]))
    bdm2 = BlockDiagMatrix(Matrix([k]), Matrix([l]))
    assert block_collapse(bdm1 + bdm2) == BlockDiagMatrix(Matrix([i + k]), Matrix([j + l]))

