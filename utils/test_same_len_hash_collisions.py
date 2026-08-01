
def test_same_len_hash_collisions(l_exp, l_add):
    length = 2 ** (l_exp + 8) + l_add
    idx = np.array([str(i) for i in range(length)], dtype=object)

    result = hash_array(idx, "utf8")
    assert not result[0] == result[1]

