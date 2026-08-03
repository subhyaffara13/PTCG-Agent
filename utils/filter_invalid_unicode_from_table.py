import logging

def filter_invalid_unicode_from_table(table):
    """
    Removes invalid unicode from table. Checks whether a table cell text contains an invalid unicode encoding. If yes,
    reset the table cell text to an empty str and log a warning for each invalid cell

    Args:
        table: table to clean.
    """
    # to do: add table id support
    if not hasattr(table, "table_id"):
        table.table_id = 0

    for row_index, row in table.iterrows():
        for col_index, cell in enumerate(row):
            cell, is_invalid = filter_invalid_unicode(cell)
            if is_invalid:
                logging.warning(
                    f"Scrub an invalid table body @ table_id: {table.table_id}, row_index: {row_index}, "
                    f"col_index: {col_index}",
                )
    for col_index, column in enumerate(table.columns):
        column, is_invalid = filter_invalid_unicode(column)
        if is_invalid:
            logging.warning(f"Scrub an invalid table header @ table_id: {table.table_id}, col_index: {col_index}")

