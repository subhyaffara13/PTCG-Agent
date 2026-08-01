
def test_mappable_2d_alpha():
    fig, ax = plt.subplots()
    x = np.arange(1, 5).reshape(2, 2)/4
    pc = ax.pcolormesh(x, alpha=x)
    cb = fig.colorbar(pc, ax=ax)
    # The colorbar's alpha should be None and the mappable should still have
    # the original alpha array
    assert cb.alpha is None
    assert pc.get_alpha() is x
    fig.draw_without_rendering()

