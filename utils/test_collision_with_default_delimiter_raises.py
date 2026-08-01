
def test_collision_with_default_delimiter_raises(ws):
    with pytest.raises(TypeError, match=".*control characters.*incompatible"):
        np.loadtxt(StringIO(f"1{ws}2{ws}3\n4{ws}5{ws}6\n"), comments=ws)
    with pytest.raises(TypeError, match=".*control characters.*incompatible"):
        np.loadtxt(StringIO(f"1{ws}2{ws}3\n4{ws}5{ws}6\n"), quotechar=ws)

