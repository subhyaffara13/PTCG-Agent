import re

def workaround_csv_sniffer_bug_last_field(sniff_line, dialect, delimiters):
    """
    Workaround for the bug https://bugs.python.org/issue30157 if is unpatched.
    """
    if csv_sniffer_has_bug_last_field():
        # Reuses code from the csv module
        right_regex = r'(?P<delim>[^\w\n"\'])(?P<space> ?)(?P<quote>["\']).*?(?P=quote)(?:$|\n)'  # noqa: E501

        for restr in (r'(?P<delim>[^\w\n"\'])(?P<space> ?)(?P<quote>["\']).*?(?P=quote)(?P=delim)',  # ,".*?",  # noqa: E501
                      r'(?:^|\n)(?P<quote>["\']).*?(?P=quote)(?P<delim>[^\w\n"\'])(?P<space> ?)',  # .*?",  # noqa: E501
                      right_regex,  # ,".*?"
                      r'(?:^|\n)(?P<quote>["\']).*?(?P=quote)(?:$|\n)'):  # ".*?" (no delim, no space)  # noqa: E501
            regexp = re.compile(restr, re.DOTALL | re.MULTILINE)
            matches = regexp.findall(sniff_line)
            if matches:
                break

        # If it does not match the expression that was bugged,
        # then this bug does not apply
        if restr != right_regex:
            return

        groupindex = regexp.groupindex

        # There is only one end of the string
        assert len(matches) == 1
        m = matches[0]

        n = groupindex['quote'] - 1
        quote = m[n]

        n = groupindex['delim'] - 1
        delim = m[n]

        n = groupindex['space'] - 1
        space = bool(m[n])

        dq_regexp = re.compile(
            rf"(({re.escape(delim)})|^)\W*{quote}[^{re.escape(delim)}\n]*{quote}[^{re.escape(delim)}\n]*{quote}\W*(({re.escape(delim)})|$)", re.MULTILINE  # noqa: E501
        )

        doublequote = bool(dq_regexp.search(sniff_line))

        dialect.quotechar = quote
        if delim in delimiters:
            dialect.delimiter = delim
        dialect.doublequote = doublequote
        dialect.skipinitialspace = space

