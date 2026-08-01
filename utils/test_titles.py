
def test_titles():
    # left and right side titles
    plt.figure()
    ax = plt.subplot(1, 1, 1)
    ax.set_title("left title", loc="left")
    ax.set_title("right title", loc="right")
    ax.set_xticks([])
    ax.set_yticks([])

