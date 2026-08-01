
def test_round_nearest():
    assert from_man_exp(0, -4, 4, round_nearest)[:3] == (0, 0, 0)
    assert from_man_exp(0xf0, -4, 4, round_nearest)[:3] == (0, 15, 0)
    assert from_man_exp(0xf7, -4, 4, round_nearest)[:3] == (0, 15, 0)
    assert from_man_exp(0xf8, -4, 4, round_nearest)[:3] == (0, 1, 4)    # 1111.1000 -> 10000.0
    assert from_man_exp(0xf9, -4, 4, round_nearest)[:3] == (0, 1, 4)    # 1111.1001 -> 10000.0
    assert from_man_exp(0xe8, -4, 4, round_nearest)[:3] == (0, 7, 1)    # 1110.1000 -> 1110.0
    assert from_man_exp(0xe9, -4, 4, round_nearest)[:3] == (0, 15, 0)     # 1110.1001 -> 1111.0
    assert from_man_exp(-0xf0, -4, 4, round_nearest)[:3] == (1, 15, 0)
    assert from_man_exp(-0xf7, -4, 4, round_nearest)[:3] == (1, 15, 0)
    assert from_man_exp(-0xf8, -4, 4, round_nearest)[:3] == (1, 1, 4)
    assert from_man_exp(-0xf9, -4, 4, round_nearest)[:3] == (1, 1, 4)
    assert from_man_exp(-0xe8, -4, 4, round_nearest)[:3] == (1, 7, 1)
    assert from_man_exp(-0xe9, -4, 4, round_nearest)[:3] == (1, 15, 0)

