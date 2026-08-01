
def test_octave_noninline():
    source = mcode((x+y)/Catalan, assign_to='me', inline=False)
    expected = (
        "Catalan = %s;\n"
        "me = (x + y)/Catalan;"
    ) % Catalan.evalf(17)
    assert source == expected

