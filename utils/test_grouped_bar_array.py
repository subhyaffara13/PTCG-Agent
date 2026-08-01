
def test_grouped_bar_array(fig_test, fig_ref):
    categories = ['A', 'B']
    array = np.array([[1, 2, 3], [1.2, 2.4, 3.6]])
    labels = ['data1', 'data2', 'data3']

    ax = fig_test.subplots()
    ax.grouped_bar(array, tick_labels=categories, labels=labels)
    ax.legend()

    ax = fig_ref.subplots()
    list_of_datasets = [column for column in array.T]
    ax.grouped_bar(list_of_datasets, tick_labels=categories, labels=labels)
    ax.legend()

