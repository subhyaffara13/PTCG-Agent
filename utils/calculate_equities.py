from typing import Any

def calculate_equities(
        hole_ranges: Iterable[Iterable[Iterable[Card]]],
        board_cards: Iterable[Card],
        hole_dealing_count: int,
        board_dealing_count: int,
        deck: Deck,
        hand_types: Iterable[type[Hand]],
        *,
        sample_count: int,
        executor: Executor | None = None,
) -> list[float]:
    """Calculate the equities.

    The user may supply an executor to use parallelization. If not
    given, a single-threaded evaluation is performed.

    >>> from concurrent.futures import ProcessPoolExecutor
    >>> from pokerkit import *
    >>> calculate_equities(
    ...     (
    ...         parse_range('33'),
    ...         parse_range('33'),
    ...     ),
    ...     Card.parse('Tc8d6h4s'),
    ...     2,
    ...     5,
    ...     Deck.STANDARD,
    ...     (StandardHighHand,),
    ...     sample_count=1000,
    ... )
    [0.5, 0.5]
    >>> calculate_equities(
    ...     (
    ...         parse_range('2h2c'),
    ...         parse_range('3h3c'),
    ...         parse_range('AhKh'),
    ...     ),
    ...     Card.parse('3s3d4c'),
    ...     2,
    ...     5,
    ...     Deck.STANDARD,
    ...     (StandardHighHand,),
    ...     sample_count=1000,
    ... )
    [0.0, 1.0, 0.0]
    >>> with ProcessPoolExecutor() as executor:
    ...     calculate_equities(
    ...         (
    ...             parse_range('2h2c'),
    ...             parse_range('3h3c'),
    ...             parse_range('AsKs'),
    ...         ),
    ...         Card.parse('QsJsTs'),
    ...         2,
    ...         5,
    ...         Deck.STANDARD,
    ...         (StandardHighHand,),
    ...         sample_count=1000,
    ...         executor=executor,
    ...     )
    ...
    [0.0, 0.0, 1.0]

    :param hole_ranges: The ranges of each player in the pot.
    :param board_cards: The board cards, may be empty.
    :param hole_dealing_count: The final number of hole cards; for
                               hold'em, it is ``2``.
    :param board_dealing_count: The final number of board cards; for
                                hold'em, it is ``5``.
    :param deck: The deck; most games typically use
                 :attr:`pokerkit.utilities.Deck.STANDARD`.
    :param hand_types: The hand types; most games typically just use
                       :class:`pokerkit.hands.StandardHighHand`.
    :param sample_count: The number of samples to simulate, higher value
                         gives greater accuracy and fidelity.
    :param executor: The optional executor, defaults to ``None`` which
                     is just using 1 thread/process. The user can supply
                     a ``ProcessPoolExecutor`` to use processes.
    :return: The equity values.
    """
    hole_ranges = tuple(map(list, map(partial(map, list), hole_ranges)))
    board_cards = list(board_cards)
    hand_types = tuple(hand_types)
    hole_cards = []
    deck_cards = []

    for selection in product(*hole_ranges):
        counter = Counter(chain(chain.from_iterable(selection), board_cards))

        if all(map(partial(eq, 1), counter.values())):
            hole_cards.append(selection)
            deck_cards.append(list(set(deck) - counter.keys()))

    fn = partial(
        __calculate_equities_1,
        hole_cards,  # type: ignore[arg-type]
        board_cards,
        hole_dealing_count,
        board_dealing_count,
        deck_cards,
        hand_types,
    )
    mapper: Any = map if executor is None else executor.map
    indices = choices(range(len(hole_cards)), k=sample_count)
    equities = [0.0] * len(hole_ranges)

    for i, equity in chain.from_iterable(map(enumerate, mapper(fn, indices))):
        equities[i] += equity

    for i, equity in enumerate(equities):
        equities[i] = equity / sample_count

    return equities

