
def test_grouped_bar_dict_of_datasets(fig_test, fig_ref):
    categories = ['A', 'B']
    data_dict = dict(data1=[1, 1.2], data2=[2, 2.4], data3=[3, 3.6])

    ax = fig_test.subplots()
    ax.grouped_bar(data_dict, tick_labels=categories)
    ax.legend()

    ax = fig_ref.subplots()
    ax.grouped_bar(data_dict.values(), tick_labels=categories, labels=data_dict.keys())
    ax.legend()

