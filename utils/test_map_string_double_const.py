
def test_map_string_double_const():
    mc = m.MapStringDoubleConst()
    mc["a"] = 10
    mc["b"] = 20.5
    assert str(mc) == "MapStringDoubleConst{a: 10, b: 20.5}"

    umc = m.UnorderedMapStringDoubleConst()
    umc["a"] = 11
    umc["b"] = 21.5

    str(umc)

