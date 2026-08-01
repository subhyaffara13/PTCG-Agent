
def test_pretty_prec():
    assert xpretty(S("0.3"), full_prec=True, wrap_line=False) == "0.300000000000000"
    assert xpretty(S("0.3"), full_prec="auto", wrap_line=False) == "0.300000000000000"
    assert xpretty(S("0.3"), full_prec=False, wrap_line=False) == "0.3"
    assert xpretty(S("0.3")*x, full_prec=True, use_unicode=False, wrap_line=False) in [
        "0.300000000000000*x",
        "x*0.300000000000000"
    ]
    assert xpretty(S("0.3")*x, full_prec="auto", use_unicode=False, wrap_line=False) in [
        "0.3*x",
        "x*0.3"
    ]
    assert xpretty(S("0.3")*x, full_prec=False, use_unicode=False, wrap_line=False) in [
        "0.3*x",
        "x*0.3"
    ]

