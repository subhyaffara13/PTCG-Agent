
def test_clipped_to_axes():
    # Ensure that _fully_clipped_to_axes() returns True under default
    # conditions for all projection types. Axes.get_tightbbox()
    # uses this to skip artists in layout calculations.
    arr = np.arange(100).reshape((10, 10))
    fig = plt.figure(figsize=(6, 2))
    ax1 = fig.add_subplot(131, projection='rectilinear')
    ax2 = fig.add_subplot(132, projection='mollweide')
    ax3 = fig.add_subplot(133, projection='polar')
    for ax in (ax1, ax2, ax3):
        # Default conditions (clipped by ax.bbox or ax.patch)
        ax.grid(False)
        h, = ax.plot(arr[:, 0])
        m = ax.pcolor(arr)
        assert h._fully_clipped_to_axes()
        assert m._fully_clipped_to_axes()
        # Non-default conditions (not clipped by ax.patch)
        rect = Rectangle((0, 0), 0.5, 0.5, transform=ax.transAxes)
        h.set_clip_path(rect)
        m.set_clip_path(rect.get_path(), rect.get_transform())
        assert not h._fully_clipped_to_axes()
        assert not m._fully_clipped_to_axes()

