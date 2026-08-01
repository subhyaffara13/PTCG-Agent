
def test_useafm():
    mpl.rcParams["ps.useafm"] = True
    fig, ax = plt.subplots()
    ax.set_axis_off()
    ax.axhline(.5)
    ax.text(.5, .5, "qk")

