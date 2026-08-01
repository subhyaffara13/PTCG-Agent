
def add_numeric_table_values(table, min_consolidation_fraction=0.7, debug_info=None):
    """
    Parses text in table column-wise and adds the consolidated values. Consolidation refers to finding values with a
    common types (date or number)

    Args:
        table:
            Table to annotate.
        min_consolidation_fraction:
            Fraction of cells in a column that need to have consolidated value.
        debug_info:
            Additional information used for logging.
    """
    table = table.copy()
    # First, filter table on invalid unicode
    filter_invalid_unicode_from_table(table)

    # Second, replace cell values by Cell objects. Cast to object dtype first: in pandas 3.x string
    # columns default to the pyarrow-backed StringDtype, which rejects writes of arbitrary Python
    # objects (it calls len(value) on the assignee, raising TypeError on the Cell dataclass).
    table = table.astype(object)
    for row_index, row in table.iterrows():
        for col_index, cell in enumerate(row):
            table.iloc[row_index, col_index] = Cell(text=cell)

    # Third, add numeric_value attributes to these Cell objects
    for col_index, column in enumerate(table.columns):
        column_values = _consolidate_numeric_values(
            _get_column_values(table, col_index),
            min_consolidation_fraction=min_consolidation_fraction,
            debug_info=(debug_info, column),
        )

        for row_index, numeric_value in column_values.items():
            table.iloc[row_index, col_index].numeric_value = numeric_value

    return table

