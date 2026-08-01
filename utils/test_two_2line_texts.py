
def test_two_2line_texts(spacing1, spacing2):
    text_string = 'line1\nline2'
    fig = plt.figure()
    renderer = fig.canvas.get_renderer()

    text1 = fig.text(0.25, 0.5, text_string, linespacing=spacing1)
    text2 = fig.text(0.25, 0.5, text_string, linespacing=spacing2)
    fig.canvas.draw()

    box1 = text1.get_window_extent(renderer=renderer)
    box2 = text2.get_window_extent(renderer=renderer)

    # line spacing only affects height
    assert box1.width == box2.width
    if spacing1 == spacing2:
        assert box1.height == box2.height
    else:
        assert box1.height != box2.height

