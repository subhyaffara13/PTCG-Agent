
def test_sdm_add():
    assert sdm_add([((1, 1, 1), QQ(1))], [((2, 0, 0), QQ(1))], lex, QQ) == \
        [((2, 0, 0), QQ(1)), ((1, 1, 1), QQ(1))]
    assert sdm_add([((1, 1, 1), QQ(1))], [((1, 1, 1), QQ(-1))], lex, QQ) == []
    assert sdm_add([((1, 0, 0), QQ(1))], [((1, 0, 0), QQ(2))], lex, QQ) == \
        [((1, 0, 0), QQ(3))]
    assert sdm_add([((1, 0, 1), QQ(1))], [((1, 1, 0), QQ(1))], lex, QQ) == \
        [((1, 1, 0), QQ(1)), ((1, 0, 1), QQ(1))]


def test_SDM_add():
    A = SDM({0:{1:ZZ(1)}, 1:{0:ZZ(2), 1:ZZ(3)}}, (2, 2), ZZ)
    B = SDM({0:{0:ZZ(1)}, 1:{0:ZZ(-2), 1:ZZ(3)}}, (2, 2), ZZ)
    C = SDM({0:{0:ZZ(1), 1:ZZ(1)}, 1:{1:ZZ(6)}}, (2, 2), ZZ)
    assert A.add(B) == B.add(A) == A + B == B + A == C

    A = SDM({0:{1:ZZ(1)}}, (2, 2), ZZ)
    B = SDM({0:{0:ZZ(1)}, 1:{0:ZZ(-2), 1:ZZ(3)}}, (2, 2), ZZ)
    C = SDM({0:{0:ZZ(1), 1:ZZ(1)}, 1:{0:ZZ(-2), 1:ZZ(3)}}, (2, 2), ZZ)
    assert A.add(B) == B.add(A) == A + B == B + A == C

    raises(TypeError, lambda: A + [])

