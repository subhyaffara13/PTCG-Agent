
def test_color_None():
    # issue 3855
    fig, ax = plt.subplots()
    ax.plot([1, 2], [1, 2], color=None)

