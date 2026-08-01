
def test_DDM_nullspace():
    # more tests are in test_nullspace.py
    A = DDM([[QQ(1), QQ(1)], [QQ(1), QQ(1)]], (2, 2), QQ)
    Anull = DDM([[QQ(-1), QQ(1)]], (1, 2), QQ)
    nonpivots = [1]
    assert A.nullspace() == (Anull, nonpivots)


def test_ddm_nullspace(name, A, A_null):
    A = A.to_field().to_ddm()
    A_null_found, _ = A.nullspace()
    _check_divided(A_null_found, A_null)

