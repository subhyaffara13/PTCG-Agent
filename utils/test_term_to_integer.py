
def test_term_to_integer():
    assert term_to_integer([1, 0, 1, 0, 0, 1, 0]) == 82
    assert term_to_integer('0010101000111001') == 10809

