
def test_pie_label_auto_align(distance, rotate):
    fig, ax = plt.subplots()
    pie = ax.pie([1, 1], startangle=45)

    texts = ax.pie_label(
        pie, ['spam', 'eggs'], distance=distance, rotate=rotate, alignment='auto')

    if distance < 1:
        for text in texts:
            # labels within the pie should be centered
            assert text.get_horizontalalignment() == 'center'
            assert text.get_verticalalignment() == 'center'

    else:
        # labels outside the pie should be aligned away from it
        h_expected = ['right', 'left']
        v_expected = ['bottom', 'top']
        for text, h_align, v_align in zip(texts, h_expected, v_expected):
            assert text.get_horizontalalignment() == h_align
            if rotate:
                assert text.get_verticalalignment() == v_align
            else:
                assert text.get_verticalalignment() == 'center'

