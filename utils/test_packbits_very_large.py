
def test_packbits_very_large():
    # test some with a larger arrays gh-8637
    # code is covered earlier but larger array makes crash on bug more likely
    for s in range(950, 1050):
        for dt in '?bBhHiIlLqQ':
            x = np.ones((200, s), dtype=bool)
            np.packbits(x, axis=1)

