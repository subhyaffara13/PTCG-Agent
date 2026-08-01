
def split_commas(value: str) -> list[str]:
    # Uses a bit smarter technique to allow last trailing comma
    # and to remove last `""` item from the split.
    items = value.split(",")
    if items and items[-1] == "":
        items.pop(-1)
    return items

