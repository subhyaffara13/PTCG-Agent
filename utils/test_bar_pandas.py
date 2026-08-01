
def test_bar_pandas(pd):
    # Smoke test for pandas
    df = pd.DataFrame(
        {'year': [2018, 2018, 2018],
         'month': [1, 1, 1],
         'day': [1, 2, 3],
         'value': [1, 2, 3]})
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

    monthly = df[['date', 'value']].groupby(['date']).sum()
    dates = monthly.index
    forecast = monthly['value']
    baseline = monthly['value']

    fig, ax = plt.subplots()
    ax.bar(dates, forecast, width=10, align='center')
    ax.plot(dates, baseline, color='orange', lw=4)

