
def test_sdm_LM():
    dic = {(1, 2, 3): QQ(1), (4, 0, 0): QQ(1), (4, 0, 1): QQ(1)}
    assert sdm_LM(sdm_from_dict(dic, lex)) == (4, 0, 1)

