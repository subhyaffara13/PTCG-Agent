
def test_grouped_bar_list_of_datasets(fig_test, fig_ref):
    categories = ['A', 'B']
    data1 = [1, 1.2]
    data2 = [2, 2.4]
    data3 = [3, 3.6]

    ax = fig_test.subplots()
    ax.grouped_bar([data1, data2, data3], tick_labels=categories,
                   labels=["data1", "data2", "data3"])
    ax.legend()

    ax = fig_ref.subplots()
    label_pos = np.array([0, 1])
    bar_width = 1 / (3 + 1.5)  # 3 bars + 1.5 group_spacing
    data_shift = -1 * bar_width + np.array([0, bar_width, 2 * bar_width])
    ax.bar(label_pos + data_shift[0], data1, width=bar_width, label="data1")
    ax.bar(label_pos + data_shift[1], data2, width=bar_width, label="data2")
    ax.bar(label_pos + data_shift[2], data3, width=bar_width, label="data3")
    ax.set_xticks(label_pos, categories)
    ax.legend()

