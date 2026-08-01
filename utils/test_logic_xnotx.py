
def test_logic_xnotx():
    assert And('a', Not('a')) == F
    assert Or('a', Not('a')) == T

