
def test_bbox_inches_tight_layout_constrained():
    fig, ax = plt.subplots(layout='constrained')
    fig.get_layout_engine().set(h_pad=0.5)
    ax.set_aspect('equal')

