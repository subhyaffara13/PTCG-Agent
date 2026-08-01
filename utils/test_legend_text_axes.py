
def test_legend_text_axes():
    fig, ax = plt.subplots()
    ax.plot([1, 2], [3, 4], label='line')
    leg = ax.legend()

    assert leg.axes is ax
    assert leg.get_texts()[0].axes is ax

