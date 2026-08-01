
def test_bc_matmul():
    assert bc_matmul(H*b1*b2*G) == BlockMatrix([[(H*G*G + H*H*H)*G]])

