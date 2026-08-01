
def test_lines_with_colors(fig_test, fig_ref, data):
    test_colors = ['red', 'green', 'blue', 'purple', 'orange']
    fig_test.add_subplot(2, 1, 1).vlines(data, 0, 1,
                                         colors=test_colors, linewidth=5)
    fig_test.add_subplot(2, 1, 2).hlines(data, 0, 1,
                                         colors=test_colors, linewidth=5)

    expect_xy = [1, 2, 3, 5]
    expect_color = ['red', 'green', 'blue', 'orange']
    fig_ref.add_subplot(2, 1, 1).vlines(expect_xy, 0, 1,
                                        colors=expect_color, linewidth=5)
    fig_ref.add_subplot(2, 1, 2).hlines(expect_xy, 0, 1,
                                        colors=expect_color, linewidth=5)

