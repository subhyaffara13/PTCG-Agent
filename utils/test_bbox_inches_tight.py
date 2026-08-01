
def test_bbox_inches_tight():
    fig, ax = plt.subplots()
    ax.imshow([[0, 1], [2, 3]])
    fig.savefig(BytesIO(), format="pdf", backend="pgf", bbox_inches="tight")


def test_bbox_inches_tight(text_placeholders):
    #: Test that a figure saved using bbox_inches='tight' is clipped correctly
    data = [[66386, 174296, 75131, 577908, 32015],
            [58230, 381139, 78045, 99308, 160454],
            [89135, 80552, 152558, 497981, 603535],
            [78415, 81858, 150656, 193263, 69638],
            [139361, 331509, 343164, 781380, 52269]]

    col_labels = ('Freeze', 'Wind', 'Flood', 'Quake', 'Hail')
    row_labels = [f'{x} year' for x in (100, 50, 20, 10, 5)]

    rows = len(data)
    ind = np.arange(len(col_labels)) + 0.3  # the x locations for the groups
    cell_text = []
    width = 0.4  # the width of the bars
    yoff = np.zeros(len(col_labels))
    # the bottom values for stacked bar chart
    fig, ax = plt.subplots(1, 1)
    for row in range(rows):
        ax.bar(ind, data[row], width, bottom=yoff, align='edge')
        yoff = yoff + data[row]
        cell_text.append([f'{x / 1000:1.1f}' for x in yoff])
    plt.xticks([])
    plt.xlim(0, 5)
    plt.legend(['1', '2', '3', '4', '5'], loc=(1.2, 0.2))
    fig.legend(['a', 'b', 'c', 'd', 'e'], bbox_to_anchor=(0, 0.2), loc='lower left')
    # Add a table at the bottom of the axes
    cell_text.reverse()
    plt.table(cellText=cell_text, rowLabels=row_labels, colLabels=col_labels,
              loc='bottom')

