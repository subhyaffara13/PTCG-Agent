
def test_transparency():
    fig, ax = plt.subplots()
    ax.set_axis_off()
    ax.plot([0, 1], color="r", alpha=0)
    ax.text(.5, .5, "foo", color="r", alpha=0)

