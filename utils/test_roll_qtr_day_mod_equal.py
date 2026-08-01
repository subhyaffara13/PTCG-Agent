
def test_roll_qtr_day_mod_equal(other, month, exp_dict, n, day_opt):
    # All cases have (other.month % 3) == (month % 3).
    expected = exp_dict.get(n, {}).get(day_opt, n)
    assert roll_qtrday(other, n, month, day_opt, modby=3) == expected

