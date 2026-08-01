
def glob_to_re(pattern):
    """Translate a shell-like glob pattern to a regular expression; return
    a string containing the regex.  Differs from 'fnmatch.translate()' in
    that '*' does not match "special characters" (which are
    platform-specific).
    """
    pattern_re = fnmatch.translate(pattern)

    # '?' and '*' in the glob pattern become '.' and '.*' in the RE, which
    # IMHO is wrong -- '?' and '*' aren't supposed to match slash in Unix,
    # and by extension they shouldn't match such "special characters" under
    # any OS.  So change all non-escaped dots in the RE to match any
    # character except the special characters (currently: just os.sep).
    sep = os.sep
    if os.sep == '\\':
        # we're using a regex to manipulate a regex, so we need
        # to escape the backslash twice
        sep = r'\\\\'
    escaped = rf'\1[^{sep}]'
    pattern_re = re.sub(r'((?<!\\)(\\\\)*)\.', escaped, pattern_re)
    return pattern_re

