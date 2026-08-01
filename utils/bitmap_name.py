
def bitmap_name(index: int) -> str:
    if index == 0:
        return "__bitmap"
    return f"__bitmap{index + 1}"

