
def collapse_consecutive_str_items(items: list[Expression]) -> list[Expression]:
    if len(items) <= 1:
        return items
    last = items[0]
    new_items = [last]
    for item in items[1:]:
        if isinstance(last, StrExpr) and isinstance(item, StrExpr):
            last.value += item.value
            last.end_line = item.end_line
            last.end_column = item.end_column
        else:
            new_items.append(item)
            last = item
    return new_items

