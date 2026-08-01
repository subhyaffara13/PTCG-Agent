
def test_text_nohandler_warning():
    """Test that Text artists with labels raise a warning"""
    fig, ax = plt.subplots()
    ax.plot([0], label="mock data")
    ax.text(x=0, y=0, s="text", label="label")
    with pytest.warns(UserWarning) as record:
        ax.legend()
    assert len(record) == 1

    # this should _not_ warn:
    f, ax = plt.subplots()
    ax.pcolormesh(np.random.uniform(0, 1, (10, 10)))
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        ax.get_legend_handles_labels()

