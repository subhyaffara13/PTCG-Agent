
def sorted_results(blocks, order=SCORE):
    '''Given a ComplexityVisitor instance, returns a list of sorted blocks
    with respect to complexity. A block is a either
    :class:`~radon.visitors.Function` object or a
    :class:`~radon.visitors.Class` object.
    The blocks are sorted in descending order from the block with the highest
    complexity.

    The optional `order` parameter indicates how to sort the blocks. It can be:

        * `LINES`: sort by line numbering;
        * `ALPHA`: sort by name (from A to Z);
        * `SCORE`: sorty by score (descending).

    Default is `SCORE`.
    '''
    return sorted(blocks, key=order)

