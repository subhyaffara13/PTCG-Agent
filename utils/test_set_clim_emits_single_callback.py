
def test_set_clim_emits_single_callback():
    data = np.array([[1, 2], [3, 4]])
    fig, ax = plt.subplots()
    image = ax.imshow(data, cmap='viridis')

    callback = unittest.mock.Mock()
    image.norm.callbacks.connect('changed', callback)

    callback.assert_not_called()

    # Call set_clim() to update the limits
    image.set_clim(1, 5)

    # Assert that only one "changed" callback is sent after calling set_clim()
    callback.assert_called_once()

