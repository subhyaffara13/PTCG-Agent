import re

def test_plot_bar_label_count_expected_fail():
    df = DataFrame(
        [(30, 10, 10, 10), (20, 20, 20, 20), (10, 30, 30, 10)], columns=list("ABCD")
    )
    error_regex = re.escape(
        "The number of titles (4) must equal the number of subplots (3)."
    )
    with pytest.raises(ValueError, match=error_regex):
        df.plot(
            subplots=[("A", "B")],
            kind="bar",
            title=["A&B", "C", "D", "Extra Title"],
        )

