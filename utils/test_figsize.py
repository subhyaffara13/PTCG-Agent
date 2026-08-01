
def test_figsize(figsize, figsize_inches):
    fig = plt.figure(figsize=figsize, dpi=100)
    assert tuple(fig.get_size_inches()) == figsize_inches

