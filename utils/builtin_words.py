
def builtin_words(names, backslash, suffix=NAME_END_RE):
    prefix = r"[\-_^]?"
    if backslash == "mandatory":
        prefix += r"\\"
    elif backslash == "optional":
        prefix += r"\\?"
    else:
        assert backslash == "disallowed"
    return words(names, prefix, suffix)

