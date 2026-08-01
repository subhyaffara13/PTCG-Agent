
def test_marker_styles():
    fig, ax = plt.subplots()
    # Since generation of the test image, None was removed but 'none' was
    # added. By moving 'none' to the front (=former sorted place of None)
    # we can avoid regenerating the test image. This can be removed if the
    # test image has to be regenerated for other reasons.
    markers = sorted(matplotlib.markers.MarkerStyle.markers,
                     key=lambda x: str(type(x))+str(x))
    markers.remove('none')
    markers = ['none', *markers]
    for y, marker in enumerate(markers):
        ax.plot((y % 2)*5 + np.arange(10)*10, np.ones(10)*10*y, linestyle='',
                marker=marker, markersize=10+y/5, label=marker)

