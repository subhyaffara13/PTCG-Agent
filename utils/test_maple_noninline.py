
def test_maple_noninline():
    source = maple_code((x + y)/Catalan, assign_to='me', inline=False)
    expected = "me := (x + y)/Catalan"

    assert source == expected

