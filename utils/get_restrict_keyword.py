
def get_restrict_keyword() -> str:
    if _IS_WINDOWS:
        # https://learn.microsoft.com/en-us/cpp/cpp/extension-restrict?view=msvc-170
        return "__restrict"
    else:
        return "__restrict__"

