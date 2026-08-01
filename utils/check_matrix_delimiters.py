
def check_matrix_delimiters(latex_str):
    """Report mismatched, excess, or missing matrix delimiters."""
    spans = []
    for begin_delim in MATRIX_DELIMS:
        end_delim = MATRIX_DELIMS[begin_delim]

        p = rcompile(begin_delim)
        q = rcompile(end_delim)

        spans.extend([(*m.span(), m.group(),
                       begin_delim) for m in p.finditer(latex_str)])
        spans.extend([(*m.span(), m.group(),
                       end_delim) for m in q.finditer(latex_str)])

    spans.sort(key=(lambda x: x[0]))
    if len(spans) % 2 == 1:
        # Odd number of delimiters; therefore something
        # is wrong. We do not complain yet; let's see if
        # we can pinpoint the actual error.
        spans.append((None, None, None, None))

    spans = [(*x, *y) for (x, y) in zip(spans[::2], spans[1::2])]
    for x in spans:
        # x is supposed to be an 8-tuple of the following form:
        #
        # (begin_delim_span_start, begin_delim_span_end,
        # begin_delim_match, begin_delim_regex,
        # end_delim_span_start, end_delim_span_end,
        # end_delim_match, end_delim_regex)

        sellipsis = "..."
        s = x[0] - 10
        if s < 0:
            s = 0
            sellipsis = ""

        eellipsis = "..."
        e = x[1] + 10
        if e > len(latex_str):
            e = len(latex_str)
            eellipsis = ""

        if x[3] in END_DELIM_REPR:
            err = (f"Extra '{x[2]}' at index {x[0]} or "
                   "missing corresponding "
                   f"'{BEGIN_DELIM_REPR[MATRIX_DELIMS_INV[x[3]]]}' "
                   f"in LaTeX string: {sellipsis}{latex_str[s:e]}"
                   f"{eellipsis}")
            raise LaTeXParsingError(err)

        if x[7] is None:
            err = (f"Extra '{x[2]}' at index {x[0]} or "
                   "missing corresponding "
                   f"'{END_DELIM_REPR[MATRIX_DELIMS[x[3]]]}' "
                   f"in LaTeX string: {sellipsis}{latex_str[s:e]}"
                   f"{eellipsis}")
            raise LaTeXParsingError(err)

        correct_end_regex = MATRIX_DELIMS[x[3]]
        sellipsis = "..." if x[0] > 0 else ""
        eellipsis = "..." if x[5] < len(latex_str) else ""
        if x[7] != correct_end_regex:
            err = ("Expected "
                   f"'{END_DELIM_REPR[correct_end_regex]}' "
                   f"to close the '{x[2]}' at index {x[0]} but "
                   f"found '{x[6]}' at index {x[4]} of LaTeX "
                   f"string instead: {sellipsis}{latex_str[x[0]:x[5]]}"
                   f"{eellipsis}")
            raise LaTeXParsingError(err)

