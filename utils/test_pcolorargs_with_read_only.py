
def test_pcolorargs_with_read_only():
    x = np.arange(6).reshape(2, 3)
    xmask = np.broadcast_to([False, True, False], x.shape)  # read-only array
    assert xmask.flags.writeable is False
    masked_x = np.ma.array(x, mask=xmask)
    plt.pcolormesh(masked_x)

    x = np.linspace(0, 1, 10)
    y = np.linspace(0, 1, 10)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(2 * np.pi * X) * np.cos(2 * np.pi * Y)
    mask = np.zeros(10, dtype=bool)
    mask[-1] = True
    mask = np.broadcast_to(mask, Z.shape)
    assert mask.flags.writeable is False
    masked_Z = np.ma.array(Z, mask=mask)
    plt.pcolormesh(X, Y, masked_Z)

    masked_X = np.ma.array(X, mask=mask)
    masked_Y = np.ma.array(Y, mask=mask)
    plt.pcolor(masked_X, masked_Y, masked_Z)

