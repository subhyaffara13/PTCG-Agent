
def _collapse_string_to_ranges(
    s: Union[str, Iterable[str]], re_escape: bool = True
) -> str:
    r"""
    Take a string or list of single-character strings, and return
    a string of the consecutive characters in that string collapsed
    into groups, as might be used in a regular expression '[a-z]'
    character set::

        'a' -> 'a' -> '[a]'
        'bc' -> 'bc' -> '[bc]'
        'defgh' -> 'd-h' -> '[d-h]'
        'fdgeh' -> 'd-h' -> '[d-h]'
        'jklnpqrtu' -> 'j-lnp-rtu' -> '[j-lnp-rtu]'

    Duplicates get collapsed out::

        'aaa' -> 'a' -> '[a]'
        'bcbccb' -> 'bc' -> '[bc]'
        'defghhgf' -> 'd-h' -> '[d-h]'
        'jklnpqrjjjtu' -> 'j-lnp-rtu' -> '[j-lnp-rtu]'

    Spaces are preserved::

        'ab c' -> ' a-c' -> '[ a-c]'

    Characters that are significant when defining regex ranges
    get escaped::

        'acde[]-' -> r'\-\[\]ac-e' -> r'[\-\[\]ac-e]'
    """

    # Developer notes:
    # - Do not optimize this code assuming that the given input string
    #   or internal lists will be short (such as in loading generators into
    #   lists to make it easier to find the last element); this method is also
    #   used to generate regex ranges for character sets in the pyparsing.unicode
    #   classes, and these can be _very_ long lists of strings

    escape_re_range_char: Callable[[str], str]
    if re_escape:
        escape_re_range_char = _escape_re_range_char
    else:
        escape_re_range_char = lambda ss: ss

    ret = []

    # reduce input string to remove duplicates, and put in sorted order
    s_chars: list[str] = sorted(set(s))

    if len(s_chars) > 2:
        # find groups of characters that are consecutive (can be collapsed
        # down to "<first>-<last>")
        for _, chars in itertools.groupby(s_chars, key=_GroupConsecutive()):
            # _ is unimportant, is just used to identify groups
            # chars is an iterator of one or more consecutive characters
            # that comprise the current group
            first = last = next(chars)
            with contextlib.suppress(ValueError):
                *_, last = chars

            if first == last:
                # there was only a single char in this group
                ret.append(escape_re_range_char(first))

            elif last == chr(ord(first) + 1):
                # there were only 2 characters in this group
                #   'a','b' -> 'ab'
                ret.append(f"{escape_re_range_char(first)}{escape_re_range_char(last)}")

            else:
                # there were > 2 characters in this group, make into a range
                #   'c','d','e' -> 'c-e'
                ret.append(
                    f"{escape_re_range_char(first)}-{escape_re_range_char(last)}"
                )
    else:
        # only 1 or 2 chars were given to form into groups
        #   'a' -> ['a']
        #   'bc' -> ['b', 'c']
        #   'dg' -> ['d', 'g']
        # no need to list them with "-", just return as a list
        # (after escaping)
        ret = [escape_re_range_char(c) for c in s_chars]

    return "".join(ret)

