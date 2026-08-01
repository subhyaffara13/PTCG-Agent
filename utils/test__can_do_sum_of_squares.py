
def test__can_do_sum_of_squares():
    assert _can_do_sum_of_squares(3, -1) is False
    assert _can_do_sum_of_squares(-3, 1) is False
    assert _can_do_sum_of_squares(0, 1)
    assert _can_do_sum_of_squares(4, 1)
    assert _can_do_sum_of_squares(1, 2)
    assert _can_do_sum_of_squares(2, 2)
    assert _can_do_sum_of_squares(3, 2) is False

