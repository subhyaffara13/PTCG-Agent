
def test_statsmodels():
    smf = pytest.importorskip("statsmodels.formula.api")

    df = DataFrame(
        {"Lottery": range(5), "Literacy": range(5), "Pop1831": range(100, 105)}
    )
    smf.ols("Lottery ~ Literacy + np.log(Pop1831)", data=df).fit()

