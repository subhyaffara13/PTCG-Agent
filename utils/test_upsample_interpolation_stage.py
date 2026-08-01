
def test_upsample_interpolation_stage(fig_test, fig_ref):
    """
    Show that interpolation_stage='auto' gives the same as 'data'
    for upsampling.
    """
    # Fixing random state for reproducibility.  This non-standard seed
    # gives red splotches for 'rgba'.
    np.random.seed(19680801+9)

    grid = np.random.rand(4, 4)
    ax = fig_ref.subplots()
    ax.imshow(grid, interpolation='bilinear', cmap='viridis',
              interpolation_stage='data')

    ax = fig_test.subplots()
    ax.imshow(grid, interpolation='bilinear', cmap='viridis',
              interpolation_stage='auto')

