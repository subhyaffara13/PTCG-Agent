
def test_annotate_offset_fontsize():
    # Test that offset_fontsize parameter works and uses accurate values
    fig, ax = plt.subplots()
    text_coords = ['offset points', 'offset fontsize']
    # 10 points should be equal to 1 fontsize unit at fontsize=10
    xy_text = [(10, 10), (1, 1)]
    anns = [ax.annotate('test', xy=(0.5, 0.5),
                        xytext=xy_text[i],
                        fontsize='10',
                        xycoords='data',
                        textcoords=text_coords[i]) for i in range(2)]
    points_coords, fontsize_coords = (ann.get_window_extent() for ann in anns)
    fig.canvas.draw()
    assert str(points_coords) == str(fontsize_coords)

