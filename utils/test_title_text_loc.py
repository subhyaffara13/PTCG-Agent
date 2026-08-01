
def test_title_text_loc():
    plt.style.use('mpl20')
    fig, ax = plt.subplots()
    np.random.seed(seed=19680808)
    pc = ax.pcolormesh(np.random.randn(10, 10))
    cb = fig.colorbar(pc, location='right', extend='max')
    cb.ax.set_title('Aardvark')
    fig.draw_without_rendering()
    # check that the title is in the proper place above the
    # colorbar axes, including its extend triangles....
    assert (cb.ax.title.get_window_extent(fig.canvas.get_renderer()).ymax >
            cb.ax.spines['outline'].get_window_extent().ymax)

