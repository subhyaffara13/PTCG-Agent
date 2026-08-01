
def test_sdm_LT():
    dic = {(1, 2, 3): QQ(1), (4, 0, 0): QQ(2), (4, 0, 1): QQ(3)}
    assert sdm_LT(sdm_from_dict(dic, lex)) == ((4, 0, 1), QQ(3))

