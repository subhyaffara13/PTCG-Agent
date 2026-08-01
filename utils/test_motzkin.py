
def test_motzkin():
    assert motzkin.is_motzkin(4) == True
    assert motzkin.is_motzkin(9) == True
    assert motzkin.is_motzkin(10) == False
    assert motzkin.find_motzkin_numbers_in_range(10,200) == [21, 51, 127]
    assert motzkin.find_motzkin_numbers_in_range(10,400) == [21, 51, 127, 323]
    assert motzkin.find_motzkin_numbers_in_range(10,1600) == [21, 51, 127, 323, 835]
    assert motzkin.find_first_n_motzkins(5) == [1, 1, 2, 4, 9]
    assert motzkin.find_first_n_motzkins(7) == [1, 1, 2, 4, 9, 21, 51]
    assert motzkin.find_first_n_motzkins(10) == [1, 1, 2, 4, 9, 21, 51, 127, 323, 835]
    raises(ValueError, lambda: motzkin.eval(77.58))
    raises(ValueError, lambda: motzkin.eval(-8))
    raises(ValueError, lambda: motzkin.find_motzkin_numbers_in_range(-2,7))
    raises(ValueError, lambda: motzkin.find_motzkin_numbers_in_range(13,7))
    raises(ValueError, lambda: motzkin.find_first_n_motzkins(112.8))

