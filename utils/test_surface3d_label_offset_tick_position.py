
def test_surface3d_label_offset_tick_position():
    ax = plt.figure().add_subplot(projection="3d")

    x, y = np.mgrid[0:6 * np.pi:0.25, 0:4 * np.pi:0.25]
    z = np.sqrt(np.abs(np.cos(x) + np.cos(y)))

    ax.plot_surface(x * 1e5, y * 1e6, z * 1e8, cmap='autumn', cstride=2, rstride=2)
    ax.set_xlabel("X label")
    ax.set_ylabel("Y label")
    ax.set_zlabel("Z label")

