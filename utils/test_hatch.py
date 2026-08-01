
def test_hatch():
    fig, ax = plt.subplots()
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, fill=False, hatch="/"))
    ax.set_xlim(0.45, 0.55)
    ax.set_ylim(0.45, 0.55)

