
def test_sdm_nullspace(name, A, A_null):
    A = A.to_field().to_sdm()
    A_null_found, _ = A.nullspace()
    _check_divided(A_null_found, A_null)


def test_SDM_nullspace():
    # More tests are in test_nullspace.py
    A = SDM({0:{0:QQ(1), 1:QQ(1)}}, (2, 2), QQ)
    assert A.nullspace()[0] == SDM({0:{0:QQ(-1), 1:QQ(1)}}, (1, 2), QQ)

