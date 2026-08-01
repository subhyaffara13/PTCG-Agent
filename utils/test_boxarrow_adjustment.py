
def test_boxarrow_adjustment():

    styles = ['larrow', 'rarrow', 'darrow']

    # Cases [head_width, head_angle] to test for each arrow style
    cases = [
        [1.5, 90],
        [1.5, 170],     # Test dynamic padding
        [0.75, 30],
        [0.5, -10],     # Should just give a rectangle
        [2, -90],
        [2, -15]        # None of arrow body is outside of head
    ]

    # Horizontal and vertical spacings of arrow centres
    spacing_horizontal = 3.75
    spacing_vertical = 1.6

    # Numbers of styles and cases
    m = len(styles)
    n = len(cases)

    figwidth = (m * spacing_horizontal)
    figheight = (n * spacing_vertical) + .5

    fig = plt.figure(figsize=(figwidth / 1.5, figheight / 1.5))

    fontsize = 0.3 * 72

    for i, stylename in enumerate(styles):
        for j, case in enumerate(cases):
            # Draw arrow
            fig.text(
                ((m - i) * spacing_horizontal - 1.5) / figwidth,
                ((n - j) * spacing_vertical - 0.5) / figheight,
                stylename, ha='center', va='center',
                size=fontsize, transform=fig.transFigure,
                bbox=dict(boxstyle=f"{stylename}, head_width={case[0]}, \
                    head_angle={case[1]}", fc="w", ec="k"))

