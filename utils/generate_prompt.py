
def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],  # unused — protocol requires it but this game is stateless across turns
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current turn."""
    turn = observation.get("current_turn", 0)
    team = _get_team(turn)
    multi_game_context = _inject_multi_game_context(observation)
    memory_context = _inject_memory_context(observation)

    my_role, opp_role = _team_role(turn)
    if _is_cluemaster(turn):
        my_remaining = _count_unrevealed_with_role(observation, my_role)
        opp_remaining = _count_unrevealed_with_role(observation, opp_role)
        prompt = f"You are the {team} Cluemaster in Word Association.\n\n"
        prompt += multi_game_context
        prompt += (
            f"Your goal is to get your team to guess all your {team} words "
            "while avoiding the opposite team's words and the trap word.\n"
        )
        prompt += (
            "The game ends as soon as either team has all of its assigned "
            "words revealed (that team wins). Your team has "
            f"{my_remaining} word(s) still hidden; the opponent has "
            f"{opp_remaining}.\n"
        )
        prompt += (
            "\nWhen your team's Guesser acts on your clue:\n"
            f"  - One of YOUR ({team}) words: revealed; the Guesser continues "
            "guessing.\n"
            "  - An OPPONENT word: revealed (advancing the opponent toward "
            "winning); the turn ends.\n"
            "  - A NEUTRAL word: revealed; the turn ends.\n"
            "  - The TRAP word: your team LOSES the game immediately.\n"
        )
        prompt += memory_context
        prompt += "Here is the board state:\n"
        prompt += _build_cluemaster_board(observation) + "\n"
        prompt += (
            "\nThink step-by-step about which unrevealed words you can "
            "connect with a single-word clue. Provide your reasoning in a "
            "'thinking' key.\n"
        )
        prompt += (
            "VALIDITY RULES FOR CLUES (violating these does NOT end the "
            "game, but a random one of your OPPONENT's still-hidden words is "
            "revealed and your turn passes — a meaningful setback):\n"
        )
        prompt += (
            "- The clue must be a SINGLE WORD. It CANNOT contain spaces or "
            "hyphens.\n"
        )
        prompt += (
            "- The clue CANNOT contain or be contained within any unrevealed "
            "word currently hidden on the board (e.g., if 'DOG' is hidden, "
            "your clue cannot be 'DOGS' or 'HOTDOG').\n"
        )
        prompt += (
            "Note on the clue number:\n"
            "- A positive number N tells the Guesser there are N words "
            "related to this clue. They receive N+1 guesses — N for the "
            "related words, plus 1 BONUS guess after correctly identifying "
            "all N (which they may spend on any remaining word from this or "
            "any previous clue).\n"
            "- 0 means 'unlimited guesses, but 0 words relate to this clue' "
            "(often used to help guessers avoid the trap or opponent words; "
            "the Guesser must still make at least one guess).\n"
            "- -1 means 'infinity' (unlimited guesses, for when you want "
            "them to guess remaining words from previous clues; the Guesser "
            "must still make at least one guess).\n"
        )
        prompt += "You MUST format your response as valid JSON like this:\n"
        prompt += (
            '{"thinking": "I see CAT and DOG, so ANIMAL connects 2 '
            'words...", "clue": "ANIMAL", "number": 2}\n'
        )
        prompt += (
            "Do not include any other text or markdown formatting outside "
            "of the JSON block."
        )
    else:
        prompt = f"You are the {team} Guesser in Word Association.\n\n"
        prompt += multi_game_context
        prompt += (
            "Your goal is to correctly guess your team's words based on the "
            "Cluemaster's clues while avoiding the opposite team's words and "
            "the trap word.\n"
        )
        prompt += (
            "The game ends as soon as either team has all of its assigned "
            "words revealed (that team wins).\n"
        )
        prompt += (
            "\nConsequences of each guess:\n"
            f"  - One of YOUR ({team}) words: revealed; you continue "
            "guessing until your guesses run out or you pass.\n"
            "  - An OPPONENT word: revealed (helping THEM win); your turn "
            "ends immediately.\n"
            "  - A NEUTRAL word: revealed; your turn ends immediately.\n"
            "  - The TRAP word: you LOSE the game immediately.\n\n"
        )
        prompt += (
            "You must make at least one guess before you are allowed to pass, "
            "or else you forfeit the game.\n"
        )
        prompt += memory_context
        prompt += _build_clue_context(observation)
        prompt += "Here is the board state:\n"
        prompt += _build_guesser_board(observation) + "\n"
        prompt += (
            "\nThink step-by-step about which unrevealed word matches the "
            "clue best. Provide your reasoning in a 'thinking' key.\n"
        )
        prompt += (
            "Then provide the integer index of the ONE word you want to guess "
            "right now in a 'guess' key.\n"
        )
        prompt += (
            "If you want to pass, set 'guess' to -1. NOTE: You are NOT "
            "allowed to pass (-1) on your very first turn without making at "
            "least one guess for the current clue, or else you forfeit the "
            "game. If you do, your action will be marked INVALID and your "
            "team will lose.\n"
        )
        prompt += "You MUST format your response as valid JSON like this:\n"
        prompt += (
            '{"thinking": "The clue is ANIMAL. Cat is at index 4, so I will '
            'guess 4...", "guess": 4}\n'
        )
        prompt += (
            "Do not include any other text or markdown formatting outside "
            "of the JSON block."
        )

    if previous_response is not None:
        prompt += RETHINK_SUFFIX.format(
            previous_response=previous_response[:500],
            previous_action=previous_action or "(could not parse)",
        )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current sub-action."""
    state = _parse_state(observation)
    num_rows, num_cols = _board_dims(state)
    board = state.get("board") or [["." for _ in range(num_cols)] for _ in range(num_rows)]
    phase = state.get("phase") or "from"
    current = state.get("current_player", "x")
    player_name = "Player 1" if current == "x" else "Player 2"
    player_glyph = "X" if current == "x" else "O"
    from_sq, to_sq = _sub_turn_squares(state, move_history, phase, num_cols)

    prompt = AMAZONS_PROMPT_TEMPLATE.format(
        num_rows=num_rows,
        num_cols=num_cols,
        player_name=player_name,
        player_glyph=player_glyph,
        phase_label=_PHASE_LABEL.get(phase, phase.upper()),
        board=_render_board(board),
        history_max_turns=_HISTORY_MAX_TURNS,
        move_history=_format_history(move_history),
        phase_instruction=_phase_instruction(phase, from_sq, to_sq),
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current arena state.

    The ``move_history`` parameter (this player's own past moves, supplied
    by core_harness) is ignored; the arena observation already exposes
    the full per-board history including the teammate's plays.
    """
    del move_history
    obs = _parse_obs(observation)
    player_id = observation.get("playerId", obs.get("your_player_id", 0))
    team_id = obs.get("your_team_id", 0)
    seat = obs.get("your_seat", 0)
    players_per_team = int(obs.get("players_per_team", 2))
    board = obs.get("board", {})
    grid_size = int(board.get("grid_size", 8))
    num_food = int(board.get("num_food", 3))
    food_collected = int(board.get("food_collected", 0))
    max_turns = int(obs.get("max_turns", 50))
    move_number = int(obs.get("move_number", 0))

    # Normalize to per-team-round units so the model isn't comparing
    # interleaved-step counts against round-based max_turns. Display is
    # 1-indexed so the final move reads "round 50 of 50"; the engine's
    # 0-indexed count would read "round 49 of 50" on the last move, and
    # models systematically misread that as "one round still remains".
    round_size = players_per_team * _NUM_TEAMS
    current_round = (move_number // round_size) + 1 if round_size else 1

    teammate_seat = (seat + 1) % players_per_team
    teammate_id = team_id * players_per_team + teammate_seat

    ant_positions = board.get("ant_positions") or {}
    your_position = ant_positions.get(str(player_id), "unknown")
    carrying = board.get("carrying_food") or {}
    is_carrying = bool(carrying.get(str(player_id), False))
    carry_status = "carrying food back to the nest" if is_carrying else "searching for food"

    grid_ascii = _render_grid_ascii(
        board.get("grid") or [],
        ant_positions,
        carrying,
        players_per_team,
        team_id,
    )
    pher_food = _sparse_pheromone(board.get("pheromone_to_food"))
    pher_nest = _sparse_pheromone(board.get("pheromone_to_nest"))
    move_history_str = _format_move_history(board.get("move_history"))

    prompt = ARENA_PROMPT_TEMPLATE.format(
        grid_size=grid_size,
        players_per_team=players_per_team,
        num_food=num_food,
        max_turns=max_turns,
        team_id=team_id,
        player_id=player_id,
        seat=seat,
        teammate_id=teammate_id,
        teammate_seat=teammate_seat,
        your_position=your_position,
        carry_status=carry_status,
        food_collected=food_collected,
        current_round=current_round,
        grid_ascii=grid_ascii,
        pher_threshold=f"{_PHEROMONE_THRESHOLD:.2f}",
        pher_food=pher_food,
        pher_nest=pher_nest,
        move_history_str=move_history_str,
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current backgammon state."""
    state = _parse_observation_payload(observation)
    player_id = int(observation.get("playerId", 0))
    my_label = _PLAYER_LABELS.get(player_id, "x")
    opp_label = "o" if my_label == "x" else "x"

    board = state.get("board") or [None] * 24
    bar = state.get("bar") or {"x": 0, "o": 0}
    off = state.get("off") or {"x": 0, "o": 0}
    dice = state.get("dice") or []
    move_number = state.get("move_number", 0)

    move_history_str = ", ".join(move_history) if move_history else "None"

    prompt = BACKGAMMON_PROMPT_TEMPLATE.format(
        dice_str=_format_dice(dice),
        move_number=move_number,
        my_bar=bar.get(my_label, 0),
        opp_bar=bar.get(opp_label, 0),
        my_off=off.get(my_label, 0),
        opp_off=off.get(opp_label, 0),
        my_points=_format_points_for_player(board, player_id, my_label),
        opp_points=_format_points_for_player(board, player_id, opp_label),
        move_history=move_history_str,
        player_id=player_id,
        my_piece=my_label,
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current bargaining state."""
    del move_history  # full offer history (both players) is in the proxy state.
    state = _parse_observation_payload(observation)
    player_id = int(observation.get("playerId", 0))

    pool = state.get("pool") or {k: 0 for k in _ITEM_KEYS}
    my_values = state.get("my_values") or {k: 0 for k in _ITEM_KEYS}
    params = state.get("params") or {}
    max_turns = int(params.get("max_turns", state.get("max_turns", 10)))
    discount = float(params.get("discount", 1.0))
    num_offers = int(state.get("num_offers", 0))
    turns_left = max(0, max_turns - num_offers)
    offer_history = state.get("offer_history") or []

    def _unit_word(n: int) -> str:
        return "unit" if n == 1 else "units"

    pool_lines = "\n".join(
        f"  {_ITEM_LABELS[k]}: {int(pool.get(k, 0))} {_unit_word(int(pool.get(k, 0)))}" for k in _ITEM_KEYS
    )
    my_value_lines = "\n".join(f"  {_ITEM_LABELS[k]}: {int(my_values.get(k, 0))}" for k in _ITEM_KEYS)
    history_str = _format_history(state)

    # Acceptance is legal only when the opponent has an open offer on the
    # table (i.e. the last event in history was their offer).
    last_offer_event = offer_history[-1] if offer_history else None
    can_accept = bool(
        last_offer_event
        and last_offer_event.get("type") == "offer"
        and int(last_offer_event.get("player", -1)) != player_id
    )
    if can_accept:
        accepted_items = last_offer_event.get("items") or {}
        you_would_receive = _complement(accepted_items, pool)
        accept_help = (
            "You MAY accept the opponent's most recent offer with"
            ' `{"action": "agree"}`. If you accept, you would receive '
            f"[{_format_items_dict(you_would_receive)}] (their offer to you)."
        )
    else:
        # Default-config bargaining alternates players strictly, so the only
        # way to land here is an empty offer_history (the opening turn).
        accept_help = (
            "No opponent offer exists yet -- you are opening, so you MUST"
            " make an offer (you cannot accept on the first turn)."
        )

    # Per OpenSpiel's bargaining.cc, the cumulative discount starts at 1 and
    # is multiplied by gamma on every move with move_number_ >= 3, i.e.
    # starting from P0's second action. So if agreement is reached after N
    # offers have been made, both players' rewards are multiplied by
    # gamma^(N-1). When gamma == 1 the rule is a no-op and we suppress the
    # paragraph to avoid prompt clutter.
    if discount < 1.0:
        discount_note = (
            f"  * Payoffs are discounted by a factor of {discount} per"
            " additional offer past the first. Accepting the very first"
            " offer is UNDISCOUNTED; if agreement is reached only after a"
            f" 2nd offer has been made, both players' payoffs are multiplied"
            f" by {discount}; after a 3rd offer, by {discount}^2; in"
            f" general, after the Nth offer, by {discount}^(N-1). Earlier"
            " acceptance preserves more reward.\n"
        )
    else:
        discount_note = ""

    prompt = BARGAINING_PROMPT_TEMPLATE.format(
        pool_lines=pool_lines,
        my_value_lines=my_value_lines,
        max_turns=max_turns,
        discount_note=discount_note,
        num_offers=num_offers,
        turns_left=turns_left,
        history_str=history_str,
        player_label=player_id + 1,
        accept_help=accept_help,
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL,
        RETHINK_UNPARSABLE,
        previous_response,
        previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    _move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current breakthrough state.

    Ignores the framework-provided per-agent ``_move_history`` -- the proxy
    surfaces a full both-player ``move_history`` in the state payload, which
    is what the model needs to reason about the position.
    """
    state = _parse_observation_payload(observation)
    player_id = observation.get("playerId", 0)

    board = state.get("board") or []
    move_number = state.get("move_number", 0)
    last_move = state.get("last_move") or "(none yet)"
    pieces = state.get("pieces") or {}
    full_history = state.get("move_history") or []

    my_piece = PIECE_BLACK if player_id == 0 else PIECE_WHITE
    opp_piece = PIECE_WHITE if player_id == 0 else PIECE_BLACK

    my_squares_list = _list_player_squares(board, my_piece)
    opp_squares_list = _list_player_squares(board, opp_piece)
    my_squares = ", ".join(my_squares_list) if my_squares_list else "(none)"
    opp_squares = ", ".join(opp_squares_list) if opp_squares_list else "(none)"

    move_history_str = ", ".join(full_history) if full_history else "None"

    # Derive board dimensions from the live state so the prompt stays
    # accurate if the game is loaded with a non-default `rows`/`columns`.
    params = state.get("params") or {}
    rows = int(params.get("rows") or state.get("rows") or len(board) or 8)
    columns = int(
        params.get("columns")
        or state.get("columns")
        or (len(board[0]) if board else 8)
    )
    if columns <= 0 or columns > 26:
        columns = max(1, min(26, columns or 8))
    file_letters = string.ascii_lowercase[:columns]
    file_range = f"{file_letters[0]}-{file_letters[-1]}" if columns > 1 else file_letters
    # OpenSpiel breakthrough fills two back ranks per side when rows >= 6
    # (see breakthrough.cc kNumRowsForFullPieces); otherwise just the very
    # back rank.
    if rows >= 6:
        black_start_ranks = f"ranks {rows - 1}-{rows}"
        white_start_ranks = "ranks 1-2"
    else:
        black_start_ranks = f"rank {rows}"
        white_start_ranks = "rank 1"

    # Black ('b') moves toward rank 1; White ('w') moves toward rank `rows`.
    forward_rank = 1 if player_id == 0 else rows

    prompt = BREAKTHROUGH_PROMPT_TEMPLATE.format(
        board_ascii=_format_board_ascii(board),
        black_count=pieces.get(PIECE_BLACK, 0),
        white_count=pieces.get(PIECE_WHITE, 0),
        player_label=player_id,
        my_piece=my_piece,
        opp_piece=opp_piece,
        my_squares=my_squares,
        opp_squares=opp_squares,
        forward_rank=forward_rank,
        move_number=move_number,
        last_move=last_move,
        move_history=move_history_str,
        rows=rows,
        columns=columns,
        file_range=file_range,
        black_start_ranks=black_start_ranks,
        white_start_ranks=white_start_ranks,
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL,
        RETHINK_UNPARSABLE,
        previous_response,
        previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current checkers state."""
    state = _parse_observation_payload(observation)
    player_id = observation.get("playerId", 0)

    board = state.get("board") or []
    move_number = state.get("move_number", 0)
    last_move_raw = state.get("last_move")
    last_move = last_move_raw or "(none yet)"
    piece_counts = state.get("piece_counts") or {}
    my_piece = "o" if player_id == 0 else "+"
    my_king = "O" if player_id == 0 else "*"
    opp_piece = "+" if player_id == 0 else "o"
    opp_king = "*" if player_id == 0 else "O"

    men, kings = _list_pieces_of(board, player_id)
    my_men_squares = ", ".join(men) if men else "(none)"
    my_king_squares = ", ".join(kings) if kings else "(none)"
    opp_men, opp_kings = _list_pieces_of(board, 1 - player_id)
    opp_men_squares = ", ".join(opp_men) if opp_men else "(none)"
    opp_king_squares = ", ".join(opp_kings) if opp_kings else "(none)"

    legal_moves = get_legal_moves(observation)
    captures_available = any(_is_capture(s) for s in legal_moves.values())
    captures_flag = "yes" if captures_available else "no"
    capture_reminder = (
        " (you MUST take a capture this turn)" if captures_available else ""
    )

    continuation_note = ""
    if (
        move_history
        and last_move_raw
        and _is_capture(move_history[-1])
        and move_history[-1].lower() == last_move_raw.lower()
    ):
        landed_square = move_history[-1][2:4].lower()
        continuation_note = (
            f"\nMulti-jump in progress: your previous capture "
            f"({move_history[-1]}) landed on {landed_square}. You must "
            f"capture again with the piece now on {landed_square} -- no "
            "other piece may move this turn. If more than one continuation "
            "jump is available, you may choose any of them.\n"
        )

    forward_rank = 8 if player_id == 0 else 1

    move_history_str = ", ".join(move_history) if move_history else "None"

    prompt = CHECKERS_PROMPT_TEMPLATE.format(
        board_ascii=_format_board_ascii(board),
        p0_men=piece_counts.get("o", 0),
        p0_kings=piece_counts.get("O", 0),
        p1_men=piece_counts.get("+", 0),
        p1_kings=piece_counts.get("*", 0),
        player_label=player_id,
        my_piece=my_piece,
        my_king=my_king,
        my_men_squares=my_men_squares,
        my_king_squares=my_king_squares,
        opp_piece=opp_piece,
        opp_king=opp_king,
        opp_men_squares=opp_men_squares,
        opp_king_squares=opp_king_squares,
        captures_flag=captures_flag,
        capture_reminder=capture_reminder,
        forward_rank=forward_rank,
        move_number=move_number,
        last_move=last_move,
        move_history=move_history_str,
        continuation_note=continuation_note,
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current chess position.

    Produces a prompt identical to GameArena's ``NO_LEGAL_ACTIONS_RETHINK_APPENDED``
    template with ``RETHINK_WITH_ENV`` strategy.
    """
    # --- Build FEN (readable state) ---
    fen = observation.get("observationString", "")

    # --- Build PGN movetext from pyspiel state ---
    serialized = observation.get("serializedGameAndState", "")
    if serialized:
        _, state = pyspiel.deserialize_game_and_state(serialized)
        pgn_movetext = _build_pgn_movetext(state)
        player_id = state.current_player()
    else:
        pgn_movetext = "None"
        player_id = observation.get("playerId", 0)

    player_name = _PLAYER_MAP.get(player_id, str(player_id))

    # --- Build rethink prompt ---
    if previous_response is not None:
        if previous_action is None:
            # Unparseable response
            rethink_prompt = BASIC_RETHINK_UNPARSABLE.format(
                generation=previous_response,
            )
        else:
            # Parsed but illegal move
            rethink_prompt = BASIC_RETHINK_ILLEGAL.format(
                last_move=previous_action,
            )
    else:
        rethink_prompt = ""

    return BASIC_PROMPT_TEMPLATE.format(
        game_short_name="chess",
        notation="Forsyth-Edwards Notation (FEN) notation",
        readable_state_str=fen,
        move_history=pgn_movetext,
        player_name=player_name,
        move_notation="standard algebraic notation (SAN)",
        rethink_prompt=rethink_prompt,
    )


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current clobber state."""
    # The per-agent `move_history` argument only contains this agent's own
    # actions. We need both players' moves, so we source the full game
    # history from the proxy's state_dict (with a serialized-state fallback).
    del move_history
    state = _parse_observation_payload(observation)
    player_id = observation.get("playerId", 0)

    rows, columns = _board_dims(state)
    board = state.get("board") or []
    full_moves = state.get("move_history")
    if not isinstance(full_moves, list):
        full_moves = _reconstruct_move_history(observation)
    last_move = state.get("last_move") or (full_moves[-1] if full_moves else None)
    last_move_str = last_move or "(none yet)"
    my_piece = "o" if player_id == 0 else "x"
    last_file = chr(ord("a") + max(0, columns - 1))

    prompt = CLOBBER_PROMPT_TEMPLATE.format(
        rows=rows,
        columns=columns,
        last_file=last_file,
        board_ascii=_format_board_ascii(board, rows, columns),
        player_label=player_id,
        my_piece=my_piece,
        move_history_str=_format_move_history(full_moves),
        last_move=last_move_str,
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current game state.

    The ``move_history`` parameter (this player's own past moves, supplied
    by core_harness) is ignored; the proxy now exposes a full per-board
    history so we can show all players' moves, not just our own.
    """
    del move_history  # see docstring
    parsed = _parse_obs(observation)
    player_id = int(observation.get("playerId", parsed.get("your_player_id", 0)))

    rows = int(parsed.get("num_rows", 8))
    cols = int(parsed.get("num_columns", 8))
    episode_length = int(parsed.get("episode_length", 20))
    moves_remaining = int(
        parsed.get(
            "moves_remaining",
            episode_length - int(parsed.get("move_number", 0)),
        )
    )
    your_pref = str(parsed.get("your_preference", "?"))

    board_str = _render_board(parsed.get("board"))

    # Curated subset of the observation — the model already has the board
    # and preference above; this slice carries only the per-player state
    # that's useful for planning.
    other_state = {
        "player_positions": parsed.get("player_positions"),
        "coins_collected": parsed.get("coins_collected"),
        "coin_colors": parsed.get("coin_colors"),
    }
    state_str = json.dumps(other_state, indent=2)

    move_history_str = _render_move_history(parsed.get("move_history"))

    prompt = COIN_PROMPT_TEMPLATE.format(
        rows=rows,
        cols=cols,
        episode_length=episode_length,
        moves_remaining=moves_remaining,
        player_id=player_id,
        your_pref=your_pref,
        board_str=board_str,
        state_str=state_str,
        move_history_str=move_history_str,
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current arena state.

    The ``move_history`` parameter (this player's own past moves, supplied
    by core_harness) is ignored; the arena observation already exposes
    the full per-board history including the teammate's plays.
    """
    del move_history
    obs = _parse_obs(observation)
    player_id = observation.get("playerId", obs.get("your_player_id", 0))
    team_id = obs.get("your_team_id", 0)
    seat = obs.get("your_seat", 0)
    your_pref = obs.get("your_preference", "?")
    rows = int(obs.get("board", {}).get("num_rows", 8))
    cols = int(obs.get("board", {}).get("num_columns", 8))
    episode_length = int(obs.get("episode_length", 20))
    players_per_team = int(obs.get("players_per_team", 2))

    teammate_seat = (seat + 1) % players_per_team
    teammate_id = team_id * players_per_team + teammate_seat

    board = obs.get("board", {})
    history = board.get("move_history") or []
    # Per-seat counts: the model is a single seat, so framing remaining
    # moves as a per-board total (which the seats split) invites a 2x
    # planning-horizon error. Surface this seat's and the teammate's
    # personal horizons instead.
    seat_played = sum(1 for entry in history if entry.get("seat") == seat)
    teammate_played = sum(
        1 for entry in history if entry.get("seat") == teammate_seat
    )
    seat_total = max(
        0, (episode_length - seat + players_per_team - 1) // players_per_team
    )
    teammate_total = max(
        0,
        (episode_length - teammate_seat + players_per_team - 1) // players_per_team,
    )
    your_move_number = seat_played + 1
    teammate_remaining = max(0, teammate_total - teammate_played)
    # Emit a compact subset of the board view to the model. No
    # moves_remaining here — it's surfaced as separate per-seat
    # sentences below to avoid a unit mismatch with episode_length.
    board_view = {
        "board": board.get("board"),
        "player_positions": board.get("player_positions"),
        "coins_collected": board.get("coins_collected"),
        "coin_colors": board.get("coin_colors"),
    }
    board_str = json.dumps(board_view, indent=2)

    if history:
        move_history_str = "\n".join(
            f"  move {idx + 1}: player {entry.get('player_id')} (seat {entry.get('seat')}) -> {entry.get('action')}"
            for idx, entry in enumerate(history)
        )
    else:
        move_history_str = "  (no moves yet)"

    prompt = ARENA_PROMPT_TEMPLATE.format(
        rows=rows,
        cols=cols,
        episode_length=episode_length,
        team_id=team_id,
        player_id=player_id,
        seat=seat,
        teammate_id=teammate_id,
        teammate_seat=teammate_seat,
        your_pref=your_pref,
        board_str=board_str,
        move_history_str=move_history_str,
        your_move_number=your_move_number,
        seat_total=seat_total,
        teammate_remaining=teammate_remaining,
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current game state."""
    serialized = observation.get("serializedGameAndState", "")
    _, state = pyspiel.deserialize_game_and_state(serialized)

    visual_board_state = state.to_string()
    params = state.get_game().get_parameters()
    rows = int(params.get("rows", 6))
    columns = int(params.get("columns", 7))
    in_a_row = int(params.get("x_in_row", 4))

    player_id = observation.get("playerId", 0)
    player_name = _PLAYER_MAP[player_id]

    rethink_prompt = ""
    if previous_response is not None:
        rethink_prompt = CONNECTX_RETHINK.format(
            generation=previous_response,
        )

    return CONNECT_X_PROMPT.format(
        rows=rows,
        columns=columns,
        in_a_row=in_a_row,
        visual_board_state=visual_board_state,
        player_name=player_name,
        max_column_index=columns - 1,
        rethink_prompt=rethink_prompt,
    )


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt rendered from the player's *own* view."""
    obs_json = _parse_observation(observation) or {}
    num_rows = obs_json.get("num_rows", 4)
    num_cols = obs_json.get("num_cols", 4)
    board = obs_json.get("board") or []

    player_id = observation.get("playerId", 0)
    player_name, player_code, connect_goal = _player_info(player_id)

    prompt = DARK_HEX_PROMPT_TEMPLATE.format(
        num_rows=num_rows,
        num_cols=num_cols,
        player_name=player_name,
        player_code=player_code,
        connect_goal=connect_goal,
        board_render=_render_board(board, num_cols),
        move_history=_format_move_history(move_history),
        last_move_line=_last_move_line(move_history),
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current dots-and-boxes state."""
    state = _parse_observation_payload(observation)
    player_id = observation.get("playerId", 0)
    player_label = 1 if player_id == 0 else 2

    num_rows = int(state.get("num_rows", 0))
    num_cols = int(state.get("num_cols", 0))
    scores = state.get("scores") or [0, 0]
    last_action = state.get("last_action")
    if last_action:
        last_move = (
            f"{last_action.get('orientation', '?')} "
            f"{last_action.get('row', '?')} {last_action.get('col', '?')}"
        )
        last_move_label = (
            "Your previous move (you completed a box, so it is your turn again)"
            if str(last_action.get("player")) == str(player_label)
            else "Opponent's last move"
        )
    else:
        last_move = "(none yet)"
        last_move_label = "Previous move"

    normalized_history = [_normalize_legal(m) or m for m in move_history]
    move_history_str = ", ".join(normalized_history) if normalized_history else "None"

    prompt = DOTS_AND_BOXES_PROMPT_TEMPLATE.format(
        num_rows=num_rows,
        num_cols=num_cols,
        rows_plus=num_rows + 1,
        cols_plus=num_cols + 1,
        rows_minus=max(num_rows - 1, 0),
        cols_minus=max(num_cols - 1, 0),
        board_ascii=_format_board_ascii(state),
        p1_score=scores[0] if len(scores) > 0 else 0,
        p2_score=scores[1] if len(scores) > 1 else 0,
        boxes_remaining=_boxes_remaining(state),
        player_label=player_label,
        last_move_label=last_move_label,
        last_move=last_move,
        move_history=move_history_str,
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current sub-action."""
    obs = _parse_observation(observation)

    player_id = observation.get("playerId", obs.get("current_player", 0)) or 0
    hand = obs.get("hands", {}).get(str(player_id), []) or []
    deadwood = (obs.get("deadwood") or {}).get(str(player_id))
    phase = obs.get("phase") or "Unknown"
    knock_card = obs.get("knock_card", "?")
    stock_size = obs.get("stock_size", "?")
    upcard = obs.get("upcard") or "(none)"
    discard_pile = obs.get("discard_pile") or []

    legal_map = get_legal_moves(observation)
    legal_strings = list(legal_map.values())

    prompt = GIN_RUMMY_PROMPT_TEMPLATE.format(
        player_glyph=_player_glyph(player_id),
        phase=phase,
        knock_card=knock_card,
        stock_size=stock_size,
        upcard=upcard,
        discard_pile=_format_discard_pile(discard_pile),
        hand_count=len(hand),
        hand=_format_hand(hand),
        deadwood=deadwood if deadwood is not None else "?",
        move_history=_format_history(move_history),
        phase_instruction=_instruction_for_phase(phase, legal_strings),
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current game state."""
    obs_string = observation.get("observationString", "")
    state = _parse_state(observation)
    board_size = _board_size_from_state(state)
    player_id = observation.get("playerId", 0)
    player_name = "Black" if player_id == 0 else "White"
    player_code = "B" if player_id == 0 else "W"

    del move_history

    prompt = GO_PROMPT_TEMPLATE.format(
        state_str=obs_string,
        ascii_board=_ascii_board_from_state(state),
        move_history=_format_full_move_history(state),
        player_name=player_name,
        player_code=player_code,
        coordinate_guidance=_coordinate_guidance(board_size),
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current game state."""
    state_str, board_size = _format_state(observation)
    if board_size <= 0:
        board_size = 8  # OpenSpiel default
    diameter = board_size * 2 - 1
    player_id = observation.get("playerId", 0)
    player_code = "x" if player_id == 0 else "o"
    player_name = "first to move" if player_id == 0 else "second to move"

    move_history_str = " ".join(move_history) if move_history else "None"

    prompt = HAVANNAH_PROMPT_TEMPLATE.format(
        board_size=board_size,
        diameter=diameter,
        state_str=state_str,
        move_history=move_history_str,
        player_code=player_code,
        player_name=player_name,
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current game state."""
    state = _parse_observation_payload(observation)
    player_id = observation.get("playerId", 0)
    player_name = "Black" if player_id == 0 else "White"
    player_code = "X" if player_id == 0 else "O"

    board = state.get("board") or []
    move_number = state.get("move_number", len(move_history))
    last_move = state.get("last_move") or "(none yet)"

    my_piece = "x" if player_id == 0 else "o"
    move_history_str = " ".join(move_history) if move_history else "None"

    prompt = LOA_PROMPT_TEMPLATE.format(
        board_ascii=_format_board_ascii(board),
        piece_line_counts=_format_piece_line_counts(board, my_piece),
        move_number=move_number,
        last_move=last_move,
        move_history=move_history_str,
        player_name=player_name,
        player_code=player_code,
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current mancala state."""
    state = _parse_observation_payload(observation)
    player_id = observation.get("playerId", 0)

    pits = state.get("pits") or {}
    p0_pits = list(pits.get("0", [0] * 6))
    p1_pits = list(pits.get("1", [0] * 6))
    stores = state.get("stores") or {}
    p0_store = stores.get("0", 0)
    p1_store = stores.get("1", 0)

    # Player 1's row is displayed right-to-left (pits 13..8) so the visual
    # layout matches a real mancala board with counter-clockwise sowing.
    p1_row_display = list(reversed(p1_pits))

    move_number = state.get("move_number", 0)
    last_action = state.get("last_action")
    last_action_player = state.get("last_action_player")
    if last_action is None:
        last_action_line = "Last action played: (none yet)."
    elif last_action_player == player_id:
        last_action_line = (
            f"Last action played: you played pit {last_action} and your last "
            f"seed landed in your own store, so it is your BONUS TURN."
        )
    elif last_action_player is not None and last_action_player >= 0:
        last_action_line = (
            f"Last action played: Opponent (Player {last_action_player}) "
            f"played pit {last_action}."
        )
    else:
        last_action_line = f"Last action played: pit {last_action}."

    move_history_str = ", ".join(move_history) if move_history else "None"

    prompt = MANCALA_PROMPT_TEMPLATE.format(
        p1_row=_format_row(p1_row_display),
        p1_store=p1_store,
        p0_store=p0_store,
        p0_row=_format_row(p0_pits),
        player_id=player_id,
        move_number=move_number,
        last_action_line=last_action_line,
        move_history=move_history_str,
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    state = _parse_observation_payload(observation)
    player_id = int(observation.get("playerId", 0))
    params = state.get("params") or {}
    num_items = int(params.get("num_items", 3))
    num_symbols = int(params.get("num_symbols", 5))
    utterance_dim = int(params.get("utterance_dim", 3))
    enable_utt = bool(params.get("enable_utterances", True))
    pool = state.get("item_pool") or [0] * num_items
    my_util = state.get("my_utilities") or [0] * num_items
    proposals = state.get("proposals") or []
    turn_type = state.get("turn_type", "proposal")
    max_steps = int(state.get("max_steps") or 7)

    pool_lines = "\n".join(f"  item {i}: {qty} units in pool" for i, qty in enumerate(pool))
    my_util_lines = "\n".join(
        f"  item {i}: {u} per unit (so a unit of item {i} is worth {u} to you)" for i, u in enumerate(my_util)
    )
    my_util_compact = "[" + ", ".join(str(u) for u in my_util) + "]"
    pool_compact = "[" + ", ".join(str(q) for q in pool) + "]"
    history_str = _format_history(state)

    if turn_type == "utterance" and enable_utt:
        # Identify the proposal this player just made (the last entry whose
        # player matches us). If it was an accept, frame it differently.
        last_proposal = "(none)"
        last_action_desc = "proposal"
        for p in reversed(proposals):
            if int(p.get("player", -1)) == player_id:
                if p.get("accept"):
                    last_proposal = "you ACCEPTED the opponent's last offer"
                    last_action_desc = "decision to ACCEPT"
                else:
                    items = p.get("items") or []
                    last_proposal = f"keep={items}"
                prompt = UTTERANCE_PROMPT_TEMPLATE.format(
                    num_items=num_items,
                    utterance_dim=utterance_dim,
                    num_symbols_m1=num_symbols - 1,
                    my_util_compact=my_util_compact,
                    pool_compact=pool_compact,
                    last_proposal=last_proposal,
                    history_str=history_str,
                    last_action_desc=last_action_desc,
                )
                break
        else:
            prompt = UTTERANCE_PROMPT_TEMPLATE.format(
                num_items=num_items,
                utterance_dim=utterance_dim,
                num_symbols_m1=num_symbols - 1,
                my_util_compact=my_util_compact,
                pool_compact=pool_compact,
                last_proposal=last_proposal,
                history_str=history_str,
                last_action_desc=last_action_desc,
            )
    else:
        # Proposal turn.
        has_open_offer = any(not p.get("accept") and int(p.get("player", -1)) != player_id for p in proposals)
        accept_help = (
            'You MAY accept the opponent\'s last proposal with `{"action": "accept"}`.'
            if has_open_offer
            else "There is no opponent proposal to accept yet -- you must propose."
        )
        utterance_note = (
            f"\n  * After each proposal you also emit a private utterance (a vector"
            f" of {utterance_dim} symbols in 0..{num_symbols - 1}). It has no"
            f" mechanical effect."
            if enable_utt
            else ""
        )
        prompt = PROPOSAL_PROMPT_TEMPLATE.format(
            num_items=num_items,
            num_items_m1=num_items - 1,
            pool_lines=pool_lines,
            my_util_lines=my_util_lines,
            max_steps=max_steps,
            utterance_note=utterance_note,
            history_str=history_str,
            player_label=player_id + 1,
            player_id=player_id,
            accept_help=accept_help,
        )

    # Move history (the harness framework already tracks this player's own
    # past action strings); fold it into a compact suffix.
    if move_history:
        prompt += "\nYour own past submissions: " + " | ".join(move_history[-6:])

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current oshi-zumo state.

    ``move_history`` contains the agent's own past bids (one entry per round
    it acted in). The opponent's per-round bid history is not available to
    the harness (core_harness only forwards this agent's own action history);
    only the opponent's current coin total appears in the prompt.
    """
    state = _parse_observation_payload(observation)
    player_id = observation.get("playerId", 0)
    coins = state.get("coins") or [0, 0]
    my_coins = coins[player_id] if player_id in (0, 1) else coins[0]
    opp_coins = coins[1 - player_id] if player_id in (0, 1) else coins[1]
    params = state.get("params") or {}

    field = state.get("field", "")
    field_size = state.get("field_size", len(field))
    wrestler_position = state.get("wrestler_position", -1)
    center = (field_size - 1) // 2
    move_number = state.get("move_number", 0)
    min_bid = int(params.get("min_bid", 0))
    horizon = int(params.get("horizon", 0))

    # Engine: wrestler_pos == 0 -> P1 wins; wrestler_pos == field_size-1 -> P0 wins.
    # So P0's losing edge is index 0 and winning edge is field_size-1; vice versa for P1.
    your_edge_index = 0 if player_id == 0 else max(field_size - 1, 0)
    opp_edge_index = max(field_size - 1, 0) if player_id == 0 else 0

    my_bids = [_bid_from_action_string(s) for s in move_history]
    my_history_str = (
        ", ".join(str(b) for b in my_bids if b is not None)
        or "(none yet)"
    )

    prompt = OSHI_ZUMO_PROMPT_TEMPLATE.format(
        field_size=field_size,
        min_bid=min_bid,
        horizon=horizon,
        field=field or "(unavailable)",
        index_row=_format_field_index_row(field_size) if field_size else "",
        wrestler_position=wrestler_position,
        center=center,
        my_coins=my_coins,
        opp_coins=opp_coins,
        move_number=move_number,
        my_history=my_history_str,
        player_label=player_id,
        your_edge_index=your_edge_index,
        opp_edge_index=opp_edge_index,
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current game state."""
    parsed = _parse_observation(observation)
    player_id = observation.get("playerId", 0)

    grid_size = int(parsed.get("grid_size", 8))
    num_ants = int(parsed.get("num_ants", 2))
    num_food = int(parsed.get("num_food", 3))
    max_turns = int(parsed.get("max_turns", 50))
    # Display is 1-indexed so the final round reads "round 50 of 50"; the
    # engine's 0-indexed ``turn`` would render "round 49 of 50" on the
    # last round, which models systematically misread as "one round still
    # remains". Mirrors the arena harness.
    display_round = int(parsed.get("turn", 0)) + 1
    score = int(parsed.get("food_collected", parsed.get("score", 0)))

    ant_positions = parsed.get("ant_positions") or []
    carrying = parsed.get("carrying_food") or []
    grid = parsed.get("grid") or [["." for _ in range(grid_size)] for _ in range(grid_size)]

    if 0 <= player_id < len(ant_positions):
        your_position = ant_positions[player_id]
    else:
        your_position = "unknown"
    carry_status = (
        "carrying food back to the nest"
        if (0 <= player_id < len(carrying) and carrying[player_id])
        else "searching for food"
    )

    grid_ascii = _render_grid_ascii(grid, ant_positions, carrying)
    pher_food = _sparse_pheromone(parsed.get("pheromone_to_food"))
    pher_nest = _sparse_pheromone(parsed.get("pheromone_to_nest"))
    ant_summary = _format_ant_summary(ant_positions, carrying)
    move_history_str = _format_move_history(parsed.get("move_history"), move_history)

    prompt = ANT_PROMPT_TEMPLATE.format(
        grid_size=grid_size,
        num_ants=num_ants,
        num_food=num_food,
        max_turns=max_turns,
        turn=display_round,
        score=score,
        player_id=player_id,
        your_position=your_position,
        carry_status=carry_status,
        grid_ascii=grid_ascii,
        pher_threshold=f"{_PHEROMONE_THRESHOLD:.2f}",
        pher_food=pher_food,
        pher_nest=pher_nest,
        ant_summary=ant_summary,
        move_history_str=move_history_str,
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt. Output is byte-identical to upstream's
    ``RepeatedPokerRethinkAgent`` + ``REPEATED_POKER`` template +
    ``RETHINK_REPEATED_POKER`` strategy.
    """
    del move_history, previous_action  # not used in repeated_poker prompts
    state = _deserialize_state(observation)
    if state is None:
        raise ValueError("Observation is missing serializedGameAndState.")
    return generate_prompt_from_state(state, previous_response=previous_response)


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current snake game state."""
    del move_history  # We render the proxy's full per-round history instead.
    player_id = int(observation.get("playerId", 0))
    parsed = _parse_observation(observation)

    rows = int(parsed.get("num_rows", 10))
    cols = int(parsed.get("num_columns", 10))
    num_players = int(parsed.get("num_players", 2))

    body_chars = ["a", "b", "c", "d"]
    head_chars = ["A", "B", "C", "D"]
    your_letter = body_chars[player_id % len(body_chars)]
    your_body_char = body_chars[player_id % len(body_chars)]
    your_head_char = head_chars[player_id % len(head_chars)]

    snakes = parsed.get("snakes") or []
    your_snake = next((s for s in snakes if int(s.get("player", -1)) == player_id), None)
    your_body = your_snake["body"] if your_snake else "(unknown)"
    your_score = your_snake["score"] if your_snake else 0
    alive = bool(your_snake.get("alive", True)) if your_snake else True
    alive_note = "" if alive else " (DEAD -- you are out of the game)"

    foods = parsed.get("foods")
    if foods is None:
        # Back-compat: older proxies emitted a single "food" key.
        single = parsed.get("food")
        foods = [single] if single else []
    food_str = ", ".join(str(f) for f in foods) if foods else "(no food on board)"

    food_respawn_interval = int(parsed.get("food_respawn_interval") or 10)
    turn = int(parsed.get("turn", 0))
    turns_until_respawn = parsed.get("turns_until_respawn")
    if turns_until_respawn is None and food_respawn_interval > 0:
        turns_until_respawn = food_respawn_interval - (turn % food_respawn_interval)

    board_str = _render_board(parsed.get("board"))
    round_history_str = _render_round_history(
        parsed.get("round_history"), num_players,
    )

    prompt = SNAKE_PROMPT_TEMPLATE.format(
        rows=rows,
        cols=cols,
        num_players=num_players,
        food_respawn_interval=food_respawn_interval,
        turns_until_respawn=turns_until_respawn,
        your_letter=your_letter,
        your_body_char=your_body_char,
        your_head_char=your_head_char,
        board_str=board_str,
        player_id=player_id,
        your_body=your_body,
        your_score=your_score,
        alive_note=alive_note,
        food_str=food_str,
        round_history_str=round_history_str,
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL, RETHINK_UNPARSABLE,
        previous_response, previous_action,
    )

    return prompt


def generate_prompt(
    observation: Mapping[str, Any],
    move_history: list[str],
    previous_response: str | None = None,
    previous_action: str | None = None,
) -> str:
    """Build the LLM prompt for the current Ultimate Tic-Tac-Toe state."""
    state = _parse_observation_payload(observation)
    player_id = observation.get("playerId", 0)

    board = state.get("board") or []
    subgrid_winners = state.get("subgrid_winners") or [""] * 9
    active_subgrid = state.get("active_subgrid")
    phase = state.get("phase", "choose_subgrid")

    my_piece = "x" if player_id == 0 else "o"
    opp_piece = "o" if player_id == 0 else "x"
    opp_player_id = 1 - player_id

    # Format phase-specific instructions and JSON templates
    if phase == "choose_subgrid":
        phase_instructions = (
            "You are currently allowed to choose ANY active local board to play in (either because it is the first turn of the game, or because your opponent's previous move sent you to a local board that is no longer active).\n"
            "A local board is active if it has not yet been won, drawn, or fully filled.\n"
            "Select one of the active local boards (index 0 to 8) to target.\n"
            "(The CRITICAL RULE about cell->board routing applies to your *next* turn, when you select a cell within this board.)"
        )
        json_format_example = (
            '```json\n{\n  "move": "<subgrid_index>"\n}\n```\nFor example: `{"move": "0"}` to choose Local Board 0.'
        )
        format_reminder = '```json\n{{\n  "move": "<subgrid_index>"\n}}\n```\nFor example: `{{"move": "0"}}`'
    elif phase == "choose_cell":
        phase_instructions = (
            f"You must play in Local Board {active_subgrid}. Choose an empty cell in Local Board {active_subgrid} to place your '{my_piece}'.\n"
            "You can specify your move either by row and column coordinates (e.g. '1,1') or by cell index (0 to 8, numbered left-to-right, top-to-bottom).\n"
            "Remember: the cell you choose (0 to 8) determines which local board your opponent must play in next."
        )
        json_format_example = (
            "```json\n"
            "{\n"
            '  "move": "<row>,<col>"\n'
            "}\n"
            "```\n"
            'For example: `{"move": "1,1"}` or `{"move": "4"}` — both choose the center cell of the local board.'
        )
        format_reminder = (
            '```json\n{{\n  "move": "<row>,<col>"\n}}\n```\nFor example: `{{"move": "1,1"}}` or `{{"move": "4"}}`'
        )
    else:
        raise ValueError(f"Invalid or terminal phase: {phase}")

    # Reconstruct history of moves from both players
    full_history = _reconstruct_move_history(observation)
    move_history_str = ", ".join(full_history) if full_history else "None"

    prompt = ULTIMATE_TIC_TAC_TOE_PROMPT_TEMPLATE.format(
        phase_instructions=phase_instructions,
        board_ascii=_format_board_ascii(board, subgrid_winners, active_subgrid),
        player_id=player_id,
        my_piece=my_piece,
        opp_piece=opp_piece,
        opp_player_id=opp_player_id,
        move_history=move_history_str,
        json_format_example=json_format_example,
    )

    rethink_unparsable_formatted = RETHINK_UNPARSABLE.format(
        previous_response="{previous_response}",
        format_reminder=format_reminder,
    )

    prompt += render_rethink_suffix(
        RETHINK_ILLEGAL,
        rethink_unparsable_formatted,
        previous_response,
        previous_action,
    )

    return prompt

