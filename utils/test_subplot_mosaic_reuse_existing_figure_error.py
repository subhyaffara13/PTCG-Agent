
def test_subplot_mosaic_reuse_existing_figure_error():
    """Test that plt.subplot_mosaic raises ValueError when reusing a figure."""
    fig = plt.figure(2)

    # 1. Test passing the existing figure number
    with pytest.raises(ValueError, match="already exists"):
        plt.subplot_mosaic([['A']], num=2)

    # 2. Test passing the actual Figure object
    with pytest.raises(ValueError, match="cannot be a FigureBase instance"):
        plt.subplot_mosaic([['A']], num=fig)

    # 3. Test that clear=True allows reuse without error
    fig_new, axd = plt.subplot_mosaic([['A']], num=2, clear=True)
    assert fig_new is fig

    plt.close(2)

