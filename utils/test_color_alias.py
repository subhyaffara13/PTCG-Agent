
def test_color_alias():
    # issues 4157 and 4162
    fig, ax = plt.subplots()
    line = ax.plot([0, 1], c='lime')[0]
    assert 'lime' == line.get_color()

