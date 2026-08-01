
def test_pandas_indexing_hist(pd):
    ser_1 = pd.Series(data=[1, 2, 2, 3, 3, 4, 4, 4, 4, 5])
    ser_2 = ser_1.iloc[1:]
    fig, ax = plt.subplots()
    ax.hist(ser_2)

