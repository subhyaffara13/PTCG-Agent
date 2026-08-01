
def test_info_show_counts(row, columns, show_counts, result):
    # Explicit cast to float to avoid implicit cast when setting nan
    df = DataFrame(1, columns=range(10), index=range(10)).astype({1: "float"})
    df.iloc[1, 1] = np.nan

    with option_context(
        "display.max_info_rows", row, "display.max_info_columns", columns
    ):
        with StringIO() as buf:
            df.info(buf=buf, show_counts=show_counts)
            assert ("non-null" in buf.getvalue()) is result

