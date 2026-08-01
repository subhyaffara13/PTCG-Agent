
def test_transform_multiple(ts):
    grouped = ts.groupby([lambda x: x.year, lambda x: x.month])
    grouped.transform(lambda x: x * 2)
    grouped.transform(np.mean)

