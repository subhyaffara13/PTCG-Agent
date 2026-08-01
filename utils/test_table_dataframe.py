
def test_table_dataframe(pd):
    # Test if Pandas Data Frame can be passed in cellText

    data = {
        'Letter': ['A', 'B', 'C'],
        'Number': [100, 200, 300]
    }

    df = pd.DataFrame(data)
    fig, ax = plt.subplots()
    table = ax.table(df, loc='center')

    for r, (index, row) in enumerate(df.iterrows()):
        for c, col in enumerate(df.columns if r == 0 else row.values):
            assert table[r if r == 0 else r+1, c].get_text().get_text() == str(col)

