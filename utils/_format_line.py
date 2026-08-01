
def _format_line(block, ranked, show_complexity=False):
    '''Format a single block as a line.

    *ranked* is the rank given by the `~radon.complexity.rank` function. If
    *show_complexity* is True, then the complexity score is added alongside.
    '''
    letter_colored = LETTERS_COLORS[block.letter] + block.letter
    rank_colored = RANKS_COLORS[ranked] + ranked
    compl = '' if not show_complexity else ' ({0})'.format(block.complexity)
    return TEMPLATE.format(
        BRIGHT,
        letter_colored,
        block.lineno,
        block.col_offset,
        block.fullname,
        rank_colored,
        compl,
        reset=RESET,
    )

