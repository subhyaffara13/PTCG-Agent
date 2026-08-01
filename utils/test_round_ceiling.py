
def test_round_ceiling():
    assert from_man_exp(0, -4, 4, round_ceiling)[:3] == (0, 0, 0)
    assert from_man_exp(0xf0, -4, 4, round_ceiling)[:3] == (0, 15, 0)
    assert from_man_exp(0xf1, -4, 4, round_ceiling)[:3] == (0, 1, 4)
    assert from_man_exp(0xff, -4, 4, round_ceiling)[:3] == (0, 1, 4)
    assert from_man_exp(-0xf0, -4, 4, round_ceiling)[:3] == (1, 15, 0)
    assert from_man_exp(-0xf1, -4, 4, round_ceiling)[:3] == (1, 15, 0)
    assert from_man_exp(-0xff, -4, 4, round_ceiling)[:3] == (1, 15, 0)

