
def test_format_hierarchical_rows_periodindex(merge_cells):
    # GH#60099
    df = DataFrame(
        {"A": [1, 2]},
        index=MultiIndex.from_arrays(
            [
                period_range(start="2006-10-06", end="2006-10-07", freq="D"),
                ["X", "Y"],
            ],
            names=["date", "category"],
        ),
    )
    formatter = ExcelFormatter(df, merge_cells=merge_cells)
    formatted_cells = formatter._format_hierarchical_rows()

    for cell in formatted_cells:
        if cell.row != 0 and cell.col == 0:
            assert isinstance(cell.val, Timestamp), (
                "Period should be converted to Timestamp"
            )

