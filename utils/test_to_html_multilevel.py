
def test_to_html_multilevel(multiindex_year_month_day_dataframe_random_data):
    ymd = multiindex_year_month_day_dataframe_random_data

    ymd.columns.name = "foo"
    ymd.to_html()
    ymd.T.to_html()

