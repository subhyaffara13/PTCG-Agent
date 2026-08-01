
def test_downsample_interpolation_stage(fig_test, fig_ref):
    """
    Show that interpolation_stage='auto' gives the same as 'rgba'
    for downsampling.
    """
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    grid = np.random.rand(400, 400)
    ax = fig_ref.subplots()
    ax.imshow(grid, interpolation='auto', cmap='viridis',
              interpolation_stage='rgba')

    ax = fig_test.subplots()
    ax.imshow(grid, interpolation='auto', cmap='viridis',
              interpolation_stage='auto')

