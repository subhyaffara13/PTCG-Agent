
def test_close():
    try:
        plt.close(1.1)
    except TypeError as e:
        assert str(e) == (
            "'fig' must be an instance of matplotlib.figure.Figure, int, str "
            "or None, not a float")

