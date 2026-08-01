
def pluralize(count: int, noun: str) -> tuple[int, str]:
    # No need to pluralize words such as `failed` or `passed`.
    if noun not in ["error", "warnings", "test"]:
        return count, noun

    # The `warnings` key is plural. To avoid API breakage, we keep it that way but
    # set it to singular here so we can determine plurality in the same way as we do
    # for `error`.
    noun = noun.replace("warnings", "warning")

    return count, noun + "s" if count != 1 else noun

