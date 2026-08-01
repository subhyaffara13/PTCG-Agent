
def test_bar_colormap(cmap):
    data = DataFrame([[1, 2], [3, 4]])
    ctx = data.style.bar(cmap=cmap, axis=None)._compute().ctx
    pubu_colors = {
        (0, 0): "#d0d1e6",
        (1, 0): "#056faf",
        (0, 1): "#73a9cf",
        (1, 1): "#023858",
    }
    for k, v in pubu_colors.items():
        assert v in ctx[k][1][1]

