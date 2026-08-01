
def test_set_aspect_negative():
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match="must be finite and positive"):
        ax.set_aspect(-1)
    with pytest.raises(ValueError, match="must be finite and positive"):
        ax.set_aspect(0)
    with pytest.raises(ValueError, match="must be finite and positive"):
        ax.set_aspect(np.inf)
    with pytest.raises(ValueError, match="must be finite and positive"):
        ax.set_aspect(-np.inf)

