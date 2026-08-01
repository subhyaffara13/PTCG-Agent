
def test_full_prec():
    assert sstr(S("0.3"), full_prec=True) == "0.300000000000000"
    assert sstr(S("0.3"), full_prec="auto") == "0.300000000000000"
    assert sstr(S("0.3"), full_prec=False) == "0.3"
    assert sstr(S("0.3")*x, full_prec=True) in [
        "0.300000000000000*x",
        "x*0.300000000000000"
    ]
    assert sstr(S("0.3")*x, full_prec="auto") in [
        "0.3*x",
        "x*0.3"
    ]
    assert sstr(S("0.3")*x, full_prec=False) in [
        "0.3*x",
        "x*0.3"
    ]

