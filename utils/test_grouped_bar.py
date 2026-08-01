
def test_grouped_bar():
    data = {
        'data1': [1, 2, 3],
        'data2': [1.2, 2.2, 3.2],
        'data3': [1.4, 2.4, 3.4],
    }

    fig, ax = plt.subplots()
    ax.grouped_bar(data, tick_labels=['A', 'B', 'C'],
                   group_spacing=0.5, bar_spacing=0.1,
                   colors=['#1f77b4', '#58a1cf', '#abd0e6'])
    ax.set_yticks([])

