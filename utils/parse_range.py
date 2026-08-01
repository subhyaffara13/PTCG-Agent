
def parse_range(
        *raw_ranges: str,
        rank_order: RankOrder = RankOrder.STANDARD,
) -> set[frozenset[Card]]:
    """Parse the range.

    The notations can be separated by a whitespace, comma, or a
    semicolon. The returned range is a set of frozensets of cards.

    >>> rng = parse_range('AKs')
    >>> len(rng)
    4
    >>> frozenset(Card.parse('AsKs')) in rng
    True
    >>> frozenset(Card.parse('AcKd')) in rng
    False

    :param raw_ranges: The raw ranges to be parsed.
    :param rank_order: The rank ordering to be used, defaults to
                       :attr:`pokerkit.utilities.RankOrder`.
    :return: The range.
    """
    raw_ranges = tuple(
        ' '.join(raw_ranges).replace(',', ' ').replace(';', ' ').split(),
    )
    range_ = set[frozenset[Card]]()

    for raw_range in raw_ranges:
        range_.update(__parse_range(raw_range, rank_order))

    return range_


def parse_range(response, **kwargs):
    """Parse range response. Used by TS.RANGE and TS.REVRANGE (legacy shape)."""
    if not response:
        return []
    # Multi-aggregator: samples have >2 elements [timestamp, val1, val2, ...]
    if len(response[0]) > 2:
        return [tuple([r[0]] + [float(v) for v in r[1:]]) for r in response]
    return [tuple((r[0], float(r[1]))) for r in response]

