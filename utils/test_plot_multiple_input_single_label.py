
def test_plot_multiple_input_single_label(label):
    # test ax.plot() with multidimensional input
    # and single label
    x = [1, 2, 3]
    y = [[1, 2],
         [2, 5],
         [4, 9]]

    fig, ax = plt.subplots()
    ax.plot(x, y, label=label)
    leg = ax.legend()
    legend_texts = [entry.get_text() for entry in leg.get_texts()]
    assert legend_texts == [str(label)] * 2

