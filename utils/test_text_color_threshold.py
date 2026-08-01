
def test_text_color_threshold(cmap, expected):
    # GH 39888
    df = DataFrame(np.arange(100).reshape(10, 10))
    result = df.style.background_gradient(cmap=cmap, axis=None)._compute().ctx
    for k in expected.keys():
        assert result[k] == expected[k]

