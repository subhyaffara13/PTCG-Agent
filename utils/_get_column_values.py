
def _get_column_values(table, col_index):
    """
    Parses text in column and returns a dict mapping row_index to values. This is the _get_column_values function from
    number_annotation_utils.py of the original implementation

    Args:
      table: Pandas dataframe
      col_index: integer, indicating the index of the column to get the numeric values of
    """
    index_to_values = {}
    for row_index, row in table.iterrows():
        text = normalize_for_match(row.iloc[col_index].text)
        index_to_values[row_index] = list(_get_numeric_values(text))
    return index_to_values

