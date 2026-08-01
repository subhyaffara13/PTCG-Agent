
def test_TR13():
    assert TR13(tan(3)*tan(2)) == -tan(2)/tan(5) - tan(3)/tan(5) + 1
    assert TR13(cot(3)*cot(2)) == 1 + cot(3)*cot(5) + cot(2)*cot(5)
    assert TR13(tan(1)*tan(2)*tan(3)) == \
        (-tan(2)/tan(5) - tan(3)/tan(5) + 1)*tan(1)
    assert TR13(tan(1)*tan(2)*cot(3)) == \
        (-tan(2)/tan(3) + 1 - tan(1)/tan(3))*cot(3)

