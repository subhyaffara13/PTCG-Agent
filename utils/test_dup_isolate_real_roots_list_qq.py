
def test_dup_isolate_real_roots_list_QQ():
    R, x = ring("x", ZZ)

    f = x**5 - 200
    g = x**5 - 201

    assert R.dup_isolate_real_roots_list([f, g]) == \
        [((QQ(75, 26), QQ(101, 35)), {0: 1}), ((QQ(309, 107), QQ(26, 9)), {1: 1})]

    R, x = ring("x", QQ)

    f = -QQ(1, 200)*x**5 + 1
    g = -QQ(1, 201)*x**5 + 1

    assert R.dup_isolate_real_roots_list([f, g]) == \
        [((QQ(75, 26), QQ(101, 35)), {0: 1}), ((QQ(309, 107), QQ(26, 9)), {1: 1})]

