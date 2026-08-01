
def test_invalid_figure_size(width, height):
    with pytest.raises(ValueError):
        plt.figure(figsize=(width, height))

    fig = plt.figure()
    with pytest.raises(ValueError):
        fig.set_size_inches(width, height)

