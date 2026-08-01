
def test_pandas_bar_align_center(pd):
    # Tests fix for issue 8767
    df = pd.DataFrame({'a': range(2), 'b': range(2)})

    fig, ax = plt.subplots(1)

    ax.bar(df.loc[df['a'] == 1, 'b'],
           df.loc[df['a'] == 1, 'b'],
           align='center')

    fig.canvas.draw()

