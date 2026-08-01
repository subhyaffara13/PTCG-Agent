
def _fold_case(info, string):
    "Folds the case of a string."
    flags = info.flags
    if (flags & _ALL_ENCODINGS) == 0:
        flags |= info.guess_encoding

    return _regex.fold_case(flags, string)

