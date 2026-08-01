
def test_imshow_endianess():
    x = np.arange(10)
    X, Y = np.meshgrid(x, x)
    Z = np.hypot(X - 5, Y - 5)

    fig, (ax1, ax2) = plt.subplots(1, 2)

    kwargs = dict(origin="lower", interpolation='nearest', cmap='viridis')

    ax1.imshow(Z.astype('<f8'), **kwargs)
    ax2.imshow(Z.astype('>f8'), **kwargs)

