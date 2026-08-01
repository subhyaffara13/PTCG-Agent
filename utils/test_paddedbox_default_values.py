
def test_paddedbox_default_values():
    # smoke test paddedbox for correct default value
    fig, ax = plt.subplots()
    at = AnchoredText("foo",  'upper left')
    pb = PaddedBox(at, patch_attrs={'facecolor': 'r'}, draw_frame=True)
    ax.add_artist(pb)
    fig.draw_without_rendering()

