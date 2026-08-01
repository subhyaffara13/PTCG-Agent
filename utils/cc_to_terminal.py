
def cc_to_terminal(results, show_complexity, min, max, total_average):
    '''Transfom Cyclomatic Complexity results into a 3-elements tuple:

        ``(res, total_cc, counted)``

    `res` is a list holding strings that are specifically formatted to be
    printed to a terminal.
    `total_cc` is a number representing the total analyzed cyclomatic
    complexity.
    `counted` holds the number of the analyzed blocks.

    If *show_complexity* is `True`, then the complexity of a block will be
    shown in the terminal line alongside its rank.
    *min* and *max* are used to control which blocks are shown in the resulting
    list. A block is formatted only if its rank is `min <= rank <= max`.
    If *total_average* is `True`, the `total_cc` and `counted` count every
    block, regardless of the fact that they are formatted in `res` or not.
    '''
    res = []
    counted = 0
    total_cc = 0.0
    for line in results:
        ranked = cc_rank(line.complexity)
        if min <= ranked <= max:
            total_cc += line.complexity
            counted += 1
            res.append(_format_line(line, ranked, show_complexity))
        elif total_average:
            total_cc += line.complexity
            counted += 1
    return res, total_cc, counted

