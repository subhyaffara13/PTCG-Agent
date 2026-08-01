
def calculate_hand_strength(
        player_count: int,
        hole_range: Iterable[Iterable[Card]],
        board_cards: Iterable[Card],
        hole_dealing_count: int,
        board_dealing_count: int,
        deck: Deck,
        hand_types: Iterable[type[Hand]],
        *,
        sample_count: int,
        executor: Executor | None = None,
) -> float:
    """Calculate the hand strength: odds of beating a single other hand
    chosen uniformly at random.

    The user may supply an executor to use parallelization. If not
    given, a single-threaded evaluation is performed.

    >>> from concurrent.futures import ProcessPoolExecutor
    >>> from pokerkit import *
    >>> calculate_hand_strength(
    ...     3,
    ...     parse_range('3h3c'),
    ...     Card.parse('3s3d2c2h'),
    ...     2,
    ...     5,
    ...     Deck.STANDARD,
    ...     (StandardHighHand,),
    ...     sample_count=1000,
    ... )
    1.0
    >>> with ProcessPoolExecutor() as executor:
    ...     calculate_hand_strength(
    ...         3,
    ...         parse_range('AsKs'),
    ...         Card.parse('QsJsTs'),
    ...         2,
    ...         5,
    ...         Deck.STANDARD,
    ...         (StandardHighHand,),
    ...         sample_count=1000,
    ...         executor=executor,
    ...     )
    ...
    1.0

    :param player_count: Number of players in the pot.
    :param hole_range: The range of the player.
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
    hole_ranges: list[Iterable[Iterable[Card]]] = [
        [[]] for _ in range(player_count - 1)
    ]

    hole_ranges.append(hole_range)

    equities = calculate_equities(
        hole_ranges,
        board_cards,
        hole_dealing_count,
        board_dealing_count,
        deck,
        hand_types,
        sample_count=sample_count,
        executor=executor,
    )

    return equities[-1]

