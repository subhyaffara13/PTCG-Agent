
def translate_pattern(glob):  # noqa: C901  # is too complex (14)  # FIXME
    """
    Translate a file path glob like '*.txt' in to a regular expression.
    This differs from fnmatch.translate which allows wildcards to match
    directory separators. It also knows about '**/' which matches any number of
    directories.
    """
    pat = ''

    # This will split on '/' within [character classes]. This is deliberate.
    chunks = glob.split(os.path.sep)

    sep = re.escape(os.sep)
    valid_char = f'[^{sep}]'

    for c, chunk in enumerate(chunks):
        last_chunk = c == len(chunks) - 1

        # Chunks that are a literal ** are globstars. They match anything.
        if chunk == '**':
            if last_chunk:
                # Match anything if this is the last component
                pat += '.*'
            else:
                # Match '(name/)*'
                pat += f'(?:{valid_char}+{sep})*'
            continue  # Break here as the whole path component has been handled

        # Find any special characters in the remainder
        i = 0
        chunk_len = len(chunk)
        while i < chunk_len:
            char = chunk[i]
            if char == '*':
                # Match any number of name characters
                pat += valid_char + '*'
            elif char == '?':
                # Match a name character
                pat += valid_char
            elif char == '[':
                # Character class
                inner_i = i + 1
                # Skip initial !/] chars
                if inner_i < chunk_len and chunk[inner_i] == '!':
                    inner_i = inner_i + 1
                if inner_i < chunk_len and chunk[inner_i] == ']':
                    inner_i = inner_i + 1

                # Loop till the closing ] is found
                while inner_i < chunk_len and chunk[inner_i] != ']':
                    inner_i = inner_i + 1

                if inner_i >= chunk_len:
                    # Got to the end of the string without finding a closing ]
                    # Do not treat this as a matching group, but as a literal [
                    pat += re.escape(char)
                else:
                    # Grab the insides of the [brackets]
                    inner = chunk[i + 1 : inner_i]
                    char_class = ''

                    # Class negation
                    if inner[0] == '!':
                        char_class = '^'
                        inner = inner[1:]

                    char_class += re.escape(inner)
                    pat += f'[{char_class}]'

                    # Skip to the end ]
                    i = inner_i
            else:
                pat += re.escape(char)
            i += 1

        # Join each chunk with the dir separator
        if not last_chunk:
            pat += sep

    pat += r'\Z'
    return re.compile(pat, flags=re.MULTILINE | re.DOTALL)


def translate_pattern(pattern, anchor=True, prefix=None, is_regex=False):
    """Translate a shell-like wildcard pattern to a compiled regular
    expression.  Return the compiled regex.  If 'is_regex' true,
    then 'pattern' is directly compiled to a regex (if it's a string)
    or just returned as-is (assumes it's a regex object).
    """
    if is_regex:
        if isinstance(pattern, str):
            return re.compile(pattern)
        else:
            return pattern

    # ditch start and end characters
    start, _, end = glob_to_re('_').partition('_')

    if pattern:
        pattern_re = glob_to_re(pattern)
        assert pattern_re.startswith(start) and pattern_re.endswith(end)
    else:
        pattern_re = ''

    if prefix is not None:
        prefix_re = glob_to_re(prefix)
        assert prefix_re.startswith(start) and prefix_re.endswith(end)
        prefix_re = prefix_re[len(start) : len(prefix_re) - len(end)]
        sep = os.sep
        if os.sep == '\\':
            sep = r'\\'
        pattern_re = pattern_re[len(start) : len(pattern_re) - len(end)]
        pattern_re = rf'{start}\A{prefix_re}{sep}.*{pattern_re}{end}'
    else:  # no prefix -- respect anchor flag
        if anchor:
            pattern_re = rf'{start}\A{pattern_re[len(start) :]}'

    return re.compile(pattern_re)

