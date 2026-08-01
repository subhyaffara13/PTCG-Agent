
def test_empty_line_plots():
    # Incompatible nr columns, plot "nothing"
    x = np.ones(10)
    y = np.ones((10, 0))
    _, ax = plt.subplots()
    line = ax.plot(x, y)
    assert len(line) == 0

    # Ensure plot([],[]) creates line
    _, ax = plt.subplots()
    line = ax.plot([], [])
    assert len(line) == 1

