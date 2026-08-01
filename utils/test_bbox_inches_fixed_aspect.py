
def test_bbox_inches_fixed_aspect():
    with plt.rc_context({'figure.constrained_layout.use': True}):
        fig, ax = plt.subplots()
        ax.plot([0, 1])
        ax.set_xlim(0, 1)
        ax.set_aspect('equal')

