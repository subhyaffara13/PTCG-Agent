
def test_bar_broadcast_args():
    fig, ax = plt.subplots()
    # Check that a bar chart with a single height for all bars works.
    ax.bar(range(4), 1)
    # Check that a horizontal chart with one width works.
    ax.barh(0, 1, left=range(4), height=1)
    # Check that edgecolor gets broadcast.
    rect1, rect2 = ax.bar([0, 1], [0, 1], edgecolor=(.1, .2, .3, .4))
    assert rect1.get_edgecolor() == rect2.get_edgecolor() == (.1, .2, .3, .4)

