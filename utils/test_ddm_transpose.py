
def test_DDM_transpose():
    ddm = DDM([[QQ(1)], [QQ(2)]], (2, 1), QQ)
    ddmT = DDM([[QQ(1), QQ(2)]], (1, 2), QQ)
    assert ddm.transpose() == ddmT
    ddm02 = DDM([], (0, 2), QQ)
    ddm02T = DDM([[], []], (2, 0), QQ)
    assert ddm02.transpose() == ddm02T
    assert ddm02T.transpose() == ddm02
    ddm0 = DDM([], (0, 0), QQ)
    assert ddm0.transpose() == ddm0


def test_ddm_transpose():
    a = [[1, 2], [3, 4]]
    assert ddm_transpose(a) == [[1, 3], [2, 4]]

