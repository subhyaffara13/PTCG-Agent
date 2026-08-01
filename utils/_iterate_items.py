
def _iterate_items(items, is_nested: bool):
    """
    Helper function to iterate over items yielding (key, item) pairs.

    For nested structures, yields ((row_index, col_index), item).
    For flat structures, yields (index, item).
    """
    if is_nested:
        for i, row in enumerate(items):
            for j, item in enumerate(row):
                yield (i, j), item
    else:
        for i, item in enumerate(items):
            yield i, item

