
def test_inset_colorbar_layout():
    fig, ax = plt.subplots(constrained_layout=True, figsize=(3, 6))
    pc = ax.imshow(np.arange(100).reshape(10, 10))
    cax = ax.inset_axes([1.02, 0.1, 0.03, 0.8])
    cb = fig.colorbar(pc, cax=cax)

    fig.draw_without_rendering()
    # make sure this is in the figure. In the colorbar swapping
    # it was being dropped from the list of children...
    np.testing.assert_allclose(cb.ax.get_position().bounds,
                               [0.87, 0.342, 0.0237, 0.315], atol=0.01)
    assert cb.ax in ax.child_axes

