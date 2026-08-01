
def make_compressed_re(
    word_list: Iterable[str],
    max_level: int = 2,
    *,
    non_capturing_groups: bool = True,
    _level: int = 1,
) -> str:
    """
    Create a regular expression string from a list of words, collapsing by common
    prefixes and optional suffixes.

    Calls itself recursively to build nested sublists for each group of suffixes
    that have a shared prefix.
    """

    def get_suffixes_from_common_prefixes(namelist: list[str]):
        if len(namelist) > 1:
            for prefix, suffixes in itertools.groupby(namelist, key=lambda s: s[:1]):
                yield prefix, sorted([s[1:] for s in suffixes], key=len, reverse=True)
        else:
            yield namelist[0][0], [namelist[0][1:]]

    if _level == 1:
        if not word_list:
            raise ValueError("no words given to make_compressed_re()")

        if "" in word_list:
            raise ValueError("word list cannot contain empty string")
    else:
        # internal recursive call, just return empty string if no words
        if not word_list:
            return ""

    # dedupe the word list
    word_list = list({}.fromkeys(word_list))

    if max_level == 0:
        if any(len(wd) > 1 for wd in word_list):
            return "|".join(
                sorted([re.escape(wd) for wd in word_list], key=len, reverse=True)
            )
        else:
            return f"[{''.join(_escape_regex_range_chars(wd) for wd in word_list)}]"

    ret = []
    sep = ""
    ncgroup = "?:" if non_capturing_groups else ""

    for initial, suffixes in get_suffixes_from_common_prefixes(sorted(word_list)):
        ret.append(sep)
        sep = "|"

        initial = re.escape(initial)

        trailing = ""
        if "" in suffixes:
            trailing = "?"
            suffixes.remove("")

        if len(suffixes) > 1:
            if all(len(s) == 1 for s in suffixes):
                ret.append(
                    f"{initial}[{''.join(_escape_regex_range_chars(s) for s in suffixes)}]{trailing}"
                )
            else:
                if _level < max_level:
                    suffix_re = make_compressed_re(
                        sorted(suffixes),
                        max_level,
                        non_capturing_groups=non_capturing_groups,
                        _level=_level + 1,
                    )
                    ret.append(f"{initial}({ncgroup}{suffix_re}){trailing}")
                else:
                    if all(len(s) == 1 for s in suffixes):
                        ret.append(
                            f"{initial}[{''.join(_escape_regex_range_chars(s) for s in suffixes)}]{trailing}"
                        )
                    else:
                        suffixes.sort(key=len, reverse=True)
                        ret.append(
                            f"{initial}({ncgroup}{'|'.join(re.escape(s) for s in suffixes)}){trailing}"
                        )
        else:
            if suffixes:
                suffix = re.escape(suffixes[0])
                if len(suffix) > 1 and trailing:
                    ret.append(f"{initial}({ncgroup}{suffix}){trailing}")
                else:
                    ret.append(f"{initial}{suffix}{trailing}")
            else:
                ret.append(initial)
    return "".join(ret)

