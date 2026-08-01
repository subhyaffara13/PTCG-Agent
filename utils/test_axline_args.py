
def test_axline_args():
    """Exactly one of *xy2* and *slope* must be specified."""
    fig, ax = plt.subplots()
    with pytest.raises(TypeError):
        ax.axline((0, 0))  # missing second parameter
    with pytest.raises(TypeError):
        ax.axline((0, 0), (1, 1), slope=1)  # redundant parameters
    ax.set_xscale('log')
    with pytest.raises(TypeError):
        ax.axline((0, 0), slope=1)
    ax.set_xscale('linear')
    ax.set_yscale('log')
    with pytest.raises(TypeError):
        ax.axline((0, 0), slope=1)
    ax.set_yscale('linear')
    with pytest.raises(ValueError):
        ax.axline((0, 0), (0, 0))  # two identical points are not allowed
        plt.draw()

