
def average_complexity(blocks):
    '''Compute the average Cyclomatic complexity from the given blocks.
    Blocks must be either :class:`~radon.visitors.Function` or
    :class:`~radon.visitors.Class`. If the block list is empty, then 0 is
    returned.
    '''
    size = len(blocks)
    if size == 0:
        return 0
    return sum((GET_COMPLEXITY(block) for block in blocks), 0.0) / len(blocks)

