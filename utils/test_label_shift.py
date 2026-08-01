
def test_label_shift():
    fig, ax = plt.subplots()

    # Test label re-centering on x-axis
    ax.set_xlabel("Test label", loc="left")
    ax.set_xlabel("Test label", loc="center")
    assert ax.xaxis.label.get_horizontalalignment() == "center"
    ax.set_xlabel("Test label", loc="right")
    assert ax.xaxis.label.get_horizontalalignment() == "right"
    ax.set_xlabel("Test label", loc="center")
    assert ax.xaxis.label.get_horizontalalignment() == "center"

    # Test label re-centering on y-axis
    ax.set_ylabel("Test label", loc="top")
    ax.set_ylabel("Test label", loc="center")
    assert ax.yaxis.label.get_horizontalalignment() == "center"
    ax.set_ylabel("Test label", loc="bottom")
    assert ax.yaxis.label.get_horizontalalignment() == "left"
    ax.set_ylabel("Test label", loc="center")
    assert ax.yaxis.label.get_horizontalalignment() == "center"

