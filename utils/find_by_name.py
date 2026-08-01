
def find_by_name(item_name, item_list):
    """
    Helper function to find item by name in a list.
        parameter item_name: name of the item.
        parameter item_list: list of items.
        return: item if found. None otherwise.
    """
    items = [item for item in item_list if item.name == item_name]
    return items[0] if len(items) > 0 else None


def find_by_name(name, item_list):
    """Helper function to find item by name in a list."""
    items = []
    for item in item_list:
        assert hasattr(item, "name"), f"{item} should have a 'name' attribute defined"  # pragma: no cover
        if item.name == name:
            items.append(item)
    if len(items) > 0:
        return items[0]
    else:
        return None

