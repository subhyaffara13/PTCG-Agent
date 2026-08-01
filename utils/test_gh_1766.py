
def test_gh_1766():
    # this should fail gracefully instead of segfaulting (int overflow)
    size = 22
    kx, ky = 3, 3
    def f2(x, y):
        return np.sin(x+y)

    x = np.linspace(0, 10, size)
    y = np.linspace(50, 700, size)
    xy = makepairs(x, y)
    tck = bisplrep(xy[0], xy[1], f2(xy[0], xy[1]), s=0, kx=kx, ky=ky)
    # the size value here can either segfault
    # or produce a MemoryError on main
    tx_ty_size = 500000
    tck[0] = np.arange(tx_ty_size)
    tck[1] = np.arange(tx_ty_size) * 4
    tt_0 = np.arange(50)
    tt_1 = np.arange(50) * 3
    with pytest.raises(MemoryError):
        bisplev(tt_0, tt_1, tck, 1, 1)

