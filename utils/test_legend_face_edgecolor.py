
def test_legend_face_edgecolor():
    # Smoke test for PolyCollection legend handler with 'face' edgecolor.
    fig, ax = plt.subplots()
    ax.fill_between([0, 1, 2], [1, 2, 3], [2, 3, 4],
                    facecolor='r', edgecolor='face', label='Fill')
    ax.legend()

