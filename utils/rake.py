
def rake(
        amount: int,
        state: State | None = None,
        *,
        percentage: float = 0,
        cap: float = inf,
        no_flop_no_drop: bool = False,
) -> tuple[int, int]:
    """Rake the amount.

    This is a default raking function used by PokerKit (which defaults
    to not raking anything). Through methods like ``functools.partial``,
    parameters like the rake percentage, cap, and no-flop-no-drop can be
    overridden.

    Note that the percentage value is expected to be within range
    [``0``, ``1``]. For instance, ``0.1`` represents 10%.

    If ``no_flop_no_drop`` is enabled, this means that a rake will only
    be collected if a flop is dealt. Since PokerKit caters to many
    variants, we interpret this as being that there exists at least one
    card on the board. Some variants do not involve board cards, so if
    this parameter is set to ``True``, no rake will be raked whatsoever.

    >>> rake(100)
    (0, 100)
    >>> rake(1000, percentage=0.1)
    (100, 900)
    >>> rake(10, percentage=0.11)
    (1, 9)
    >>> rake(10.0, percentage=0.11)
    (1.1, 8.9)
    >>> rake(10.0, percentage=0.11, cap=1.0)
    (1.0, 9.0)
    >>> rake(100, percentage=0.1, no_flop_no_drop=True)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: If no-flop-no-drop is enabled, the state must be checked, bu...

    When this function is actually called, the ``state`` parameter will
    not be ``None`` as it is by default. This argument can be used to
    encode a more complicated raking logic.

    During state creation, user can supply their own rake function,
    corresponding with the accepted type signature.

    :param amount: The pot amount.
    :param state: The optional poker state whose pot is being raked.
    :param percentage: The rake percentage, defaults to ``0``. It should
                       be between ``0`` (0%) and ``1`` (100%).
    :param cap: The maximum raked amount, defaults to ``math.inf``
                (unlimited).
    :param no_flop_no_drop: ``True`` to only rake when there are cards
                            on the board, ``False`` otherwise. Defaults
                            to ``False``.
    :return: The raked amount and the unraked amount.
    """
    if not 0 <= percentage <= 1:
        raise ValueError(
            'The rake percentage ({percentage}) should be between 0 and 1.',
        )

    if no_flop_no_drop:
        if state is None:
            raise ValueError(
                (
                    'If no-flop-no-drop is enabled, the state must be checked,'
                    ' but it is unavailable.'
                ),
            )

        if not any(state.board_cards):
            return 0, amount

    raked_amount = amount * percentage

    if isinstance(amount, Integral):
        raked_amount = round(raked_amount)

    raked_amount = min(raked_amount, cap)
    unraked_amount = amount - raked_amount

    return cast(tuple[int, int], (raked_amount, unraked_amount))

