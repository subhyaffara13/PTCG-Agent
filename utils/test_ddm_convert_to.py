
def test_DDM_convert_to():
    ddm = DDM([[ZZ(1), ZZ(2)]], (1, 2), ZZ)
    assert ddm.convert_to(ZZ) == ddm
    ddmq = ddm.convert_to(QQ)
    assert ddmq.domain == QQ

