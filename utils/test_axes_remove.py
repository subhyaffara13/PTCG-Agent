
def test_axes_remove():
    """Removing the colorbar's axes should also remove the colorbar"""
    fig, ax = plt.subplots()
    sc = ax.scatter([1, 2], [3, 4])
    cb = fig.colorbar(sc)

    with mock.patch.object(cb, 'remove') as mock_cb_remove:
        cb.ax.remove()

    mock_cb_remove.assert_called()


def test_axes_remove():
    fig, axs = plt.subplots(2, 2)
    axs[-1, -1].remove()
    for ax in axs.ravel()[:-1]:
        assert ax in fig.axes
    assert axs[-1, -1] not in fig.axes
    assert len(fig.axes) == 3

