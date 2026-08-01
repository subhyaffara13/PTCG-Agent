
def test_pcolormesh():
    # Remove this line when this test image is regenerated.
    plt.rcParams['pcolormesh.snap'] = False

    n = 12
    x = np.linspace(-1.5, 1.5, n)
    y = np.linspace(-1.5, 1.5, n*2)
    X, Y = np.meshgrid(x, y)
    Qx = np.cos(Y) - np.cos(X)
    Qz = np.sin(Y) + np.sin(X)
    Qx = (Qx + 1.1)
    Z = np.hypot(X, Y) / 5
    Z = (Z - Z.min()) / np.ptp(Z)

    # The color array can include masked values:
    Zm = ma.masked_where(np.abs(Qz) < 0.5 * np.max(Qz), Z)

    _, (ax1, ax2, ax3) = plt.subplots(1, 3)
    ax1.pcolormesh(Qx, Qz, Zm[:-1, :-1], lw=0.5, edgecolors='k')
    ax2.pcolormesh(Qx, Qz, Zm[:-1, :-1], lw=2, edgecolors=['b', 'w'])
    ax3.pcolormesh(Qx, Qz, Zm, shading="gouraud")

