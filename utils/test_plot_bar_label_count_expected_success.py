
def test_plot_bar_label_count_expected_success():
    df = DataFrame(
        [(30, 10, 10, 10), (20, 20, 20, 20), (10, 30, 30, 10)], columns=list("ABCD")
    )
    df.plot(subplots=[("A", "B", "D")], kind="bar", title=["A&B&D", "C"])

