
def parse_action(
        state: State,
        action: str,
        parse_value: Callable[[str], int] = parse_value,
) -> None:
    """Parse the action.

    :param state: The state.
    :param action: The string action.
    :param parse_value: The value parsing function.
    :return: ``None``.
    """

    def get_player_index() -> int:
        label, parsed_index = player[:1], int(player[1:]) - 1

        if label != 'p':
            raise ValueError(f'{repr(player)} is not a valid player label.')

        return parsed_index

    def verify_player(index: int | None) -> None:
        if get_player_index() != index:
            raise ValueError(
                (
                    f'The player {repr(player)} is not a valid player for the'
                    f' action {repr(action)}.'
                ),
            )

    commentary = action[action.index('#') + 2:] if '#' in action else None
    words = action.split()

    if '#' in words:
        words = words[:words.index('#')]

    match words:
        case 'd', 'db', cards:
            state.deal_board(cards)
        case 'd', 'dh', player, cards:
            state.deal_hole(
                cards,
                get_player_index(),
                commentary=commentary,
            )
        case player, 'sd':
            verify_player(state.stander_pat_or_discarder_index)
            state.stand_pat_or_discard(commentary=commentary)
        case player, 'sd', cards:
            verify_player(state.stander_pat_or_discarder_index)
            state.stand_pat_or_discard(cards, commentary=commentary)
        case player, 'pb':
            verify_player(state.actor_index)
            state.post_bring_in(commentary=commentary)
        case player, 'f':
            verify_player(state.actor_index)
            state.fold(commentary=commentary)
        case player, 'cc':
            verify_player(state.actor_index)
            state.check_or_call(commentary=commentary)
        case player, 'cbr', amount:
            verify_player(state.actor_index)
            state.complete_bet_or_raise_to(
                parse_value(amount),
                commentary=commentary,
            )
        case player, 'sm':
            state.show_or_muck_hole_cards(
                False,
                get_player_index(),
                commentary=commentary,
            )
        case player, 'sm', '-':
            state.show_or_muck_hole_cards(
                True,
                get_player_index(),
                commentary=commentary,
            )
        case player, 'sm', cards:
            state.show_or_muck_hole_cards(
                cards,
                get_player_index(),
                commentary=commentary,
            )
        case ():
            state.no_operate(commentary=commentary)
        case _:
            raise ValueError(
                f'The action {repr(action)} is an invalid action.',
            )

