
def format_item_name_list(s: Iterable[str]) -> str:
    lst = list(s)
    if len(lst) <= 5:
        return "(" + ", ".join([f'"{name}"' for name in lst]) + ")"
    else:
        return "(" + ", ".join([f'"{name}"' for name in lst[:5]]) + ", ...)"

