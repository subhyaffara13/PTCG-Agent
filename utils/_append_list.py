
def _append_list(dest_list: list[str], src_list: list[str]) -> None:
    dest_list.extend(copy.deepcopy(item) for item in src_list)

