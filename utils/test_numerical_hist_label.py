
def test_numerical_hist_label():
    fig, ax = plt.subplots()
    ax.hist([range(15)] * 5, label=range(5))
    ax.legend()

