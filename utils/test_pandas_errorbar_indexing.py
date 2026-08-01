
def test_pandas_errorbar_indexing(pd):
    df = pd.DataFrame(np.random.uniform(size=(5, 4)),
                      columns=['x', 'y', 'xe', 'ye'],
                      index=[1, 2, 3, 4, 5])
    fig, ax = plt.subplots()
    ax.errorbar('x', 'y', xerr='xe', yerr='ye', data=df)

