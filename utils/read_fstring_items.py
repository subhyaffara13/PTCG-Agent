
def read_fstring_items(state: State, data: ReadBuffer) -> Expression:
    n = read_int(data)
    items = [read_fstring_item(state, data) for _ in range(n)]
    return build_fstring_join(data, items)

