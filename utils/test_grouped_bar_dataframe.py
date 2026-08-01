
def test_grouped_bar_dataframe(fig_test, fig_ref, pd):
    categories = ['A', 'B']
    labels = ['data1', 'data2', 'data3']
    df = pd.DataFrame([[1, 2, 3], [1.2, 2.4, 3.6]],
                      index=categories, columns=labels)

    ax = fig_test.subplots()
    ax.grouped_bar(df)
    ax.legend()

    ax = fig_ref.subplots()
    list_of_datasets = [df[col].to_numpy() for col in df.columns]
    ax.grouped_bar(list_of_datasets, tick_labels=categories, labels=labels)
    ax.legend()

