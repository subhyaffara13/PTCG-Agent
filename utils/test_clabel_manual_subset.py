
def test_clabel_manual_subset():
    fig, ax = plt.subplots()
    cs = ax.contour([[1, 2], [3, 4]], levels=[1.5, 2.5, 3.5])
    # Attempt to label only one specific level manually
    ax.clabel(cs, levels=[2.5], manual=[(0.5, 0.5)])

