
def test_orient_dcm():
    cxx, cyy, czz = dynamicsymbols('c_{xx}, c_{yy}, c_{zz}')
    cxy, cxz, cyx = dynamicsymbols('c_{xy}, c_{xz}, c_{yx}')
    cyz, czx, czy = dynamicsymbols('c_{yz}, c_{zx}, c_{zy}')
    B_C_A = Matrix([[cxx, cxy, cxz],
                    [cyx, cyy, cyz],
                    [czx, czy, czz]])
    A = ReferenceFrame('A')
    B = ReferenceFrame('B')
    B.orient_dcm(A, B_C_A)
    assert B.dcm(A) == Matrix([[cxx, cxy, cxz],
                               [cyx, cyy, cyz],
                               [czx, czy, czz]])

