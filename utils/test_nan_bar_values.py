
def test_nan_bar_values():
    fig, ax = plt.subplots()
    ax.bar([0, 1], [np.nan, 4])

