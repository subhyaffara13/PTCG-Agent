
def test_bar_pandas_indexed(pd):
    # Smoke test for indexed pandas
    df = pd.DataFrame({"x": [1., 2., 3.], "width": [.2, .4, .6]},
                      index=[1, 2, 3])
    fig, ax = plt.subplots()
    ax.bar(df.x, 1., width=df.width)

