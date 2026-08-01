
def test_hamming_unequal_length_with_w():
    u = [0, 0, 1]
    v = [0, 0, 1]
    w = [1, 0, 1, 0]
    msg = "'w' should have the same length as 'u' and 'v'."
    with pytest.raises(ValueError, match=msg):
        whamming(u, v, w)

