
def _formatArray(a, format_function, line_width, next_line_prefix,
                 separator, edge_items, summary_insert, legacy):
    """formatArray is designed for two modes of operation:

    1. Full output

    2. Summarized output

    """
    def recurser(index, hanging_indent, curr_width):
        """
        By using this local function, we don't need to recurse with all the
        arguments. Since this function is not created recursively, the cost is
        not significant
        """
        axis = len(index)
        axes_left = a.ndim - axis

        if axes_left == 0:
            return format_function(a[index])

        # when recursing, add a space to align with the [ added, and reduce the
        # length of the line by 1
        next_hanging_indent = hanging_indent + ' '
        if legacy <= 113:
            next_width = curr_width
        else:
            next_width = curr_width - len(']')

        a_len = a.shape[axis]
        show_summary = summary_insert and 2 * edge_items < a_len
        if show_summary:
            leading_items = edge_items
            trailing_items = edge_items
        else:
            leading_items = 0
            trailing_items = a_len

        # stringify the array with the hanging indent on the first line too
        s = ''

        # last axis (rows) - wrap elements if they would not fit on one line
        if axes_left == 1:
            # the length up until the beginning of the separator / bracket
            if legacy <= 113:
                elem_width = curr_width - len(separator.rstrip())
            else:
                elem_width = curr_width - max(
                    len(separator.rstrip()), len(']')
                )

            line = hanging_indent
            for i in range(leading_items):
                word = recurser(index + (i,), next_hanging_indent, next_width)
                s, line = _extendLine_pretty(
                    s, line, word, elem_width, hanging_indent, legacy)
                line += separator

            if show_summary:
                s, line = _extendLine(
                    s, line, summary_insert, elem_width, hanging_indent, legacy
                )
                if legacy <= 113:
                    line += ", "
                else:
                    line += separator

            for i in range(trailing_items, 1, -1):
                word = recurser(index + (-i,), next_hanging_indent, next_width)
                s, line = _extendLine_pretty(
                    s, line, word, elem_width, hanging_indent, legacy)
                line += separator

            if legacy <= 113:
                # width of the separator is not considered on 1.13
                elem_width = curr_width
            word = recurser(index + (-1,), next_hanging_indent, next_width)
            s, line = _extendLine_pretty(
                s, line, word, elem_width, hanging_indent, legacy)

            s += line

        # other axes - insert newlines between rows
        else:
            s = ''
            line_sep = separator.rstrip() + '\n' * (axes_left - 1)

            for i in range(leading_items):
                nested = recurser(
                    index + (i,), next_hanging_indent, next_width
                )
                s += hanging_indent + nested + line_sep

            if show_summary:
                if legacy <= 113:
                    # trailing space, fixed nbr of newlines,
                    # and fixed separator
                    s += hanging_indent + summary_insert + ", \n"
                else:
                    s += hanging_indent + summary_insert + line_sep

            for i in range(trailing_items, 1, -1):
                nested = recurser(index + (-i,), next_hanging_indent,
                                  next_width)
                s += hanging_indent + nested + line_sep

            nested = recurser(index + (-1,), next_hanging_indent, next_width)
            s += hanging_indent + nested

        # remove the hanging indent, and wrap in []
        s = '[' + s[len(hanging_indent):] + ']'
        return s

    try:
        # invoke the recursive part with an initial index and prefix
        return recurser(index=(),
                        hanging_indent=next_line_prefix,
                        curr_width=line_width)
    finally:
        # recursive closures have a cyclic reference to themselves, which
        # requires gc to collect (gh-10620). To avoid this problem, for
        # performance, we break the cycle:
        recurser = None

