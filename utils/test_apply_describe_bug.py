
def test_apply_describe_bug(multiindex_dataframe_random_data):
    grouped = multiindex_dataframe_random_data.groupby(level="first")
    grouped.describe()  # it works!

