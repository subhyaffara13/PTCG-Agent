
def test_orient_explicit():
    cxx, cyy, czz = dynamicsymbols('c_{xx}, c_{yy}, c_{zz}')
    cxy, cxz, cyx = dynamicsymbols('c_{xy}, c_{xz}, c_{yx}')
    cyz, czx, czy = dynamicsymbols('c_{yz}, c_{zx}, c_{zy}')
    dcxx, dcyy, dczz = dynamicsymbols('c_{xx}, c_{yy}, c_{zz}', 1)
    dcxy, dcxz, dcyx = dynamicsymbols('c_{xy}, c_{xz}, c_{yx}', 1)
    dcyz, dczx, dczy = dynamicsymbols('c_{yz}, c_{zx}, c_{zy}', 1)
    A = ReferenceFrame('A')
    B = ReferenceFrame('B')
    B_C_A = Matrix([[cxx, cxy, cxz],
                    [cyx, cyy, cyz],
                    [czx, czy, czz]])
    B_w_A = ((cyx*dczx + cyy*dczy + cyz*dczz)*B.x +
            (czx*dcxx + czy*dcxy + czz*dcxz)*B.y +
            (cxx*dcyx + cxy*dcyy + cxz*dcyz)*B.z)
    A.orient_explicit(B, B_C_A)
    assert B.dcm(A) == B_C_A
    assert A.ang_vel_in(B) == B_w_A
    assert B.ang_vel_in(A) == -B_w_A

