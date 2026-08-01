
def test_paddedbox():
    fig, ax = plt.subplots()

    ta = TextArea("foo")
    pb = PaddedBox(ta, pad=5, patch_attrs={'facecolor': 'r'}, draw_frame=True)
    ab = AnchoredOffsetbox('upper left', child=pb)
    ax.add_artist(ab)

    ta = TextArea("bar")
    pb = PaddedBox(ta, pad=10, patch_attrs={'facecolor': 'b'})
    ab = AnchoredOffsetbox('upper right', child=pb)
    ax.add_artist(ab)

    ta = TextArea("foobar")
    pb = PaddedBox(ta, pad=15, draw_frame=True)
    ab = AnchoredOffsetbox('lower right', child=pb)
    ax.add_artist(ab)

