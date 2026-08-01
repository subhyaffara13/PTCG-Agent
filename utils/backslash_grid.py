
def backslash_grid(**interface: Any) -> str:
    interface["indent"] = interface["white_space"][:-1]
    return hanging_indent(**interface)

