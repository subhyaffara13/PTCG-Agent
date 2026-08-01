
def _remove_duplication_in_list(orig_list: list[str]) -> list[str]:
    new_list: list[str] = []
    for item in orig_list:
        if item not in new_list:
            new_list.append(item)
    return new_list

