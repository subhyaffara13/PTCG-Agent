
def test_reblock_2x2():
    B = BlockMatrix([[MatrixSymbol('A_%d%d'%(i,j), 2, 2)
                            for j in range(3)]
                            for i in range(3)])
    assert B.blocks.shape == (3, 3)

    BB = reblock_2x2(B)
    assert BB.blocks.shape == (2, 2)

    assert B.shape == BB.shape
    assert B.as_explicit() == BB.as_explicit()

