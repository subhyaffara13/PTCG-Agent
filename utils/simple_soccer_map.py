
def simple_soccer_map(xs=6, ys=9):
    assert xs % 2 == 0, "xs must be even"
    smap = np.zeros((xs, ys), dtype=np.int32)
    smap[0 : xs / 2 - 1, 0] = -1
    smap[xs / 2 + 1 : xs, 0] = -1
    smap[0 : xs / 2 - 1, ys - 1] = -1
    smap[xs / 2 + 1 : xs, ys - 1] = -1
    return smap

