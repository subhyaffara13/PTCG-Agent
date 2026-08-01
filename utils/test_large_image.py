
def test_large_image(fig_test, fig_ref, dim, size, msg, origin, high_memory):
    # Check that Matplotlib downsamples images that are too big for AGG
    # See issue #19276. Currently the fix only works for png output but not
    # pdf or svg output.
    ax_test = fig_test.subplots()
    ax_ref = fig_ref.subplots()

    array = np.zeros((1, size + 2))
    array[:, array.size // 2:] = 1
    if dim == 'col':
        array = array.T
    im = ax_test.imshow(array, vmin=0, vmax=1,
                        aspect='auto', extent=(0, 1, 0, 1),
                        interpolation='none',
                        origin=origin)

    with pytest.warns(UserWarning,
                      match=f'Data with more than {msg} cannot be '
                      'accurately displayed.'):
        with io.BytesIO() as buffer:
            # Write to a buffer to trigger the warning
            fig_test.savefig(buffer)

    array = np.zeros((1, size // 2 + 1))
    array[:, array.size // 2:] = 1
    if dim == 'col':
        array = array.T
    im = ax_ref.imshow(array, vmin=0, vmax=1, aspect='auto',
                       extent=(0, 1, 0, 1),
                       interpolation='none',
                       origin=origin)

