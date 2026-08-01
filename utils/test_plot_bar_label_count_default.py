
def test_plot_bar_label_count_default():
    df = DataFrame(
        [(30, 10, 10, 10), (20, 20, 20, 20), (10, 30, 30, 10)], columns=list("ABCD")
    )
    df.plot(subplots=True, kind="bar", title=["A", "B", "C", "D"])

