
def test_pandas_iterable(pd):
    # Using a list or series yields equivalent
    # colormaps, i.e the series isn't seen as
    # a single color
    lst = ['red', 'blue', 'green']
    s = pd.Series(lst)
    cm1 = mcolors.ListedColormap(lst)
    cm2 = mcolors.ListedColormap(s)
    assert_array_equal(cm1.colors, cm2.colors)

