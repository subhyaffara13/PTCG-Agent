
def test_control_character_newline_raises(nl):
    txt = StringIO(f"1{nl}2{nl}3{nl}{nl}4{nl}5{nl}6{nl}{nl}")
    msg = "control character.*cannot be a newline"
    with pytest.raises(TypeError, match=msg):
        np.loadtxt(txt, delimiter=nl)
    with pytest.raises(TypeError, match=msg):
        np.loadtxt(txt, comments=nl)
    with pytest.raises(TypeError, match=msg):
        np.loadtxt(txt, quotechar=nl)

