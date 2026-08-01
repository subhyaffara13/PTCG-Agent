
def test_subclass(fig_test, fig_ref):
    class subdate(datetime):
        pass

    fig_test.subplots().plot(subdate(2000, 1, 1), 0, "o")
    fig_ref.subplots().plot(datetime(2000, 1, 1), 0, "o")

