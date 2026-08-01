
def test_bar_color_precedence():
    # Test the precedence of 'color' and 'facecolor' in bar plots
    fig, ax = plt.subplots()

    # case 1: no color specified
    bars = ax.bar([1, 2, 3], [4, 5, 6])
    for bar in bars:
        assert mcolors.same_color(bar.get_facecolor(), 'blue')

    # case 2: Only 'color'
    bars = ax.bar([11, 12, 13], [4, 5, 6], color='red')
    for bar in bars:
        assert mcolors.same_color(bar.get_facecolor(), 'red')

    # case 3: Only 'facecolor'
    bars = ax.bar([21, 22, 23], [4, 5, 6], facecolor='yellow')
    for bar in bars:
        assert mcolors.same_color(bar.get_facecolor(), 'yellow')

    # case 4: 'facecolor' and 'color'
    bars = ax.bar([31, 32, 33], [4, 5, 6], color='red', facecolor='green')
    for bar in bars:
        assert mcolors.same_color(bar.get_facecolor(), 'green')

