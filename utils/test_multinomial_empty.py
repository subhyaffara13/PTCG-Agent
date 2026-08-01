
def test_multinomial_empty():
    # gh-20483
    # Ensure that empty p-vals are correctly handled
    assert random.multinomial(10, []).shape == (0,)
    assert random.multinomial(3, [], size=(7, 5, 3)).shape == (7, 5, 3, 0)

