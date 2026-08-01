
def parse_acpc_line(
    line: str,
    cfg: Config,
    policy: SeatingPolicy,
    button_index: int | None = None,
    hand_id_override: str | None = None,
) -> tuple[Hand, ParseState]:
  """Parses a single line from an ACPC hand history log.

  Args:
      line: The single line string from the log, starting with "STATE:".
      cfg: The Config object specifying game parameters.
      policy: The SeatingPolicy to use for blind and action order.
      button_index: The index of the player with the button. Required for
          `ButtonPolicy`, ignored for `LegacyACPCPolicy`.
      hand_id_override: If provided, this hand ID will be used instead of the
          one found in the ACPC line.

  Returns:
      A Hand object containing the parsed information.

  Raises:
      ValueError: If the line format is invalid or inconsistent with the config.
  """
  parts = line.strip().split(":")
  if len(parts) != 6 or parts[0] != "STATE":
    raise ValueError(f"Line is not a valid ACPC STATE with 6 parts: {line}")
  _, hand_num, actions_blob, cards_blob, profits_blob, players_blob = parts

  player_ids = players_blob.split("|")
  if len(player_ids) != cfg.seats:
    raise ValueError(
        f"Seat count mismatch: config seats={cfg.seats}, log has"
        f" {len(player_ids)} players"
    )

  # Parse cards
  cards_by_street = cards_blob.split("/")
  hole = cards_by_street[0].split("|")
  if len(hole) != cfg.seats:
    raise ValueError("Hole cards count does not match seats")
  hole_cards: list[tuple[Card, Card]] = []
  for h in hole:
    cs = [Card(x) for x in textwrap.wrap(h, 2) if x]
    if len(cs) != 2:
      raise ValueError("Each player must have exactly two hole cards")
    hole_cards.append((cs[0], cs[1]))

  community: list[list[Card]] = []
  for chunk in cards_by_street[1:]:
    cards = [Card(x) for x in textwrap.wrap(chunk, 2) if x]
    community.append(cards)

  # Profits / winners
  if profits_blob:
    profits = [int(float(p)) for p in profits_blob.split("|")]
    winners = [i for i, v in enumerate(profits) if v > 0]
  else:
    profits = []
    winners = []

  # Players
  players = [
      Player(id=pid, seat=i, stack_start=cfg.starting_stacks[i])
      for i, pid in enumerate(player_ids)
  ]

  # Seating policy selection
  if isinstance(policy, LegacyACPCPolicy):
    # Legacy ignores button
    b_idx = 0
  else:
    if button_index is None:
      raise ValueError("Button index is required for non-legacy policies")
    b_idx = button_index % cfg.seats

  # Prepare parse state
  ps = ParseState(
      street=Street.BLINDS,
      table_max=0,
      prev_street_max=0,
      contrib_street=[0] * cfg.seats,
      contrib_total=[0] * cfg.seats,
      active=[True] * cfg.seats,
      all_in=[False] * cfg.seats,
      last_aggressor=None,
      uncalled_amount=0,
  )

  events: list[Event] = []

  # Antes first (if any)
  if cfg.ante > 0:
    for p in range(cfg.seats):
      _apply_delta(ps, p, cfg.ante, cfg)
      events.append(Event(
          Street.BLINDS, p, ActionKind.ANTE, to_amount=cfg.ante, delta=cfg.ante
      ))

  # Blinds
  sb_idx, bb_idx = policy.blind_indices(cfg, b_idx)
  _apply_delta(ps, sb_idx, cfg.small_blind, cfg)
  ps.table_max = max(ps.table_max, cfg.small_blind)
  ps.contrib_street[sb_idx] = cfg.small_blind
  events.append(Event(
      Street.BLINDS, sb_idx, ActionKind.SB, to_amount=cfg.small_blind,
      delta=cfg.small_blind
  ))

  _apply_delta(ps, bb_idx, cfg.big_blind, cfg)
  ps.table_max = max(ps.table_max, cfg.big_blind)
  ps.contrib_street[bb_idx] = cfg.big_blind
  events.append(Event(
      Street.BLINDS,
      bb_idx,
      ActionKind.BB,
      to_amount=cfg.big_blind,
      delta=cfg.big_blind
  ))

  # Streets actions
  # preflop/flop/turn/river (some may be empty)
  streets_text = actions_blob.split("/")
  street_map = [Street.PREFLOP, Street.FLOP, Street.TURN, Street.RIVER]

  for s_idx, text in enumerate(streets_text):
    ps.street = street_map[s_idx] if s_idx < len(street_map) else Street.RIVER
    order = policy.action_order(cfg, b_idx, ps.street)
    if not text:
      # Move to next street: freeze table_max
      _advance_street(ps)
      continue
    tokens = tokenize_actions(text)
    # iterator over order cycling, but skip folded/all-in players
    cur_pos = 0
    # can_check if no wager yet this street (table_max equals prev_street_max
    # except preflop where prev_street_max is BB)
    # We'll determine checks by comparing needed delta to 0.
    for tok, amount in tokens:
      # Find next actor
      steps = 0
      while steps < cfg.seats and (
          not ps.active[order[cur_pos]] or ps.all_in[order[cur_pos]]
      ):
        cur_pos = (cur_pos + 1) % cfg.seats
        steps += 1
      actor = order[cur_pos]

      if tok == "f":
        ps.active[actor] = False
        events.append(Event(ps.street, actor, ActionKind.FOLD))
      elif tok == "c":
        need = max(ps.table_max - ps.contrib_street[actor], 0)
        if need == 0:
          events.append(Event(ps.street, actor, ActionKind.CHECK))
        else:
          _apply_delta(ps, actor, need, cfg)
          ps.uncalled_amount = 0
          events.append(Event(ps.street, actor, ActionKind.CALL, delta=need))
      elif tok == "r":
        assert amount is not None and amount >= 0
        # ACPC for OpenSpiel: amount = total chips committed during hand.
        chips_this_action = amount - ps.contrib_total[actor]
        if chips_this_action < 0:
          raise ValueError(
              f"Raise to {amount} is less than current commitment "
              f"{ps.contrib_total[actor]}"
          )

        kind = ActionKind.BET if ps.table_max == 0 else ActionKind.RAISE

        _apply_delta(ps, actor, chips_this_action, cfg)

        street_total_after_action = ps.contrib_street[actor]

        if kind == ActionKind.BET:
          event_delta = street_total_after_action
          event_to_amount = street_total_after_action
        else:  # ActionKind.RAISE
          event_delta = street_total_after_action - ps.table_max
          event_to_amount = street_total_after_action

        if event_delta < 0 and kind == ActionKind.RAISE:
          raise ValueError("Non-monotonic raise detected")

        ps.uncalled_amount = street_total_after_action - ps.table_max
        ps.table_max = street_total_after_action
        ps.last_aggressor = actor

        events.append(
            Event(
                ps.street,
                actor,
                kind,
                to_amount=event_to_amount,
                delta=event_delta,
                all_in=ps.all_in[actor],
            )
        )
      else:
        raise ValueError("Unknown token")

      # advance seat
      cur_pos = (cur_pos + 1) % cfg.seats

    # next street
    _advance_street(ps)

  # Derive folded summary for renderer
  summary_folded = [not a for a in ps.active]

  # Compute uncalled receiver and adjust pot contributions for side-pot calc
  uncalled_amount = ps.uncalled_amount
  uncalled_receiver = ps.last_aggressor if uncalled_amount > 0 else None

  hand = Hand(
      hand_id=hand_id_override if hand_id_override is not None else hand_num,
      config=cfg,
      players=players,
      button_index=None if isinstance(policy, LegacyACPCPolicy) else b_idx,
      hole_cards=hole_cards,
      community=community,
      events=events,
      winners=winners,
      profits=profits,
      uncalled_amount=uncalled_amount,
      uncalled_receiver=uncalled_receiver,
      summary_folded=summary_folded,
  )
  return hand, ps

