
def test_julia_noninline():
    source = julia_code((x+y)/Catalan, assign_to='me', inline=False)
    expected = (
        "const Catalan = %s\n"
        "me = (x + y) / Catalan"
    ) % Catalan.evalf(17)
    assert source == expected

