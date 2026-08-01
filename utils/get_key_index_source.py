
def get_key_index_source(source: Any, index: Any) -> str:
    return f"list(dict.keys({source}))[{index}]"

