
def test_coeff_search():
    C = []
    search = coeff_search(2, 1)
    for i, c in enumerate(search):
        C.append(c)
        if i == 12:
            break
    assert C == [[1, 1], [1, 0], [1, -1], [0, 1], [2, 2], [2, 1], [2, 0], [2, -1], [2, -2], [1, 2], [1, -2], [0, 2], [3, 3]]

