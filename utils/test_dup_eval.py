
def test_dup_eval():
    assert dup_eval([], 7, ZZ) == 0
    assert dup_eval([1, 2], 0, ZZ) == 2
    assert dup_eval([1, 2, 3], 7, ZZ) == 66

