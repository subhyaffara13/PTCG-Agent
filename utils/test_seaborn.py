
def test_seaborn(mpl_cleanup):
    seaborn = pytest.importorskip("seaborn")
    tips = DataFrame(
        {"day": pd.date_range("2023", freq="D", periods=5), "total_bill": range(5)}
    )
    seaborn.stripplot(x="day", y="total_bill", data=tips)

