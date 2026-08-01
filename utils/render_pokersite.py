
def render_pokersite(
    hand: Hand,
    observer_id: str | None = None,
    sitename: str = "",
) -> str:
  """Renders a Hand object into a hand history using a similar format as various poker sites.

  Args:
    hand: The Hand object to render.
    observer_id: If provided, only the hole cards of the player with this ID
      will be shown. Otherwise, all hole cards are shown.
    sitename: If provided, this string will be included in the header. With
      appropriate sitenames, the output can be handled by popular poker
      software.

  Returns:
    A multi-line string hand history.
  """
  cfg = hand.config

  lines: list[str] = []
  sitename_prefix = f"{sitename} " if sitename else ""
  top_line = (
      f"{sitename_prefix}Hand #{int(hand.hand_id)}: Hold'em No Limit"
      f" ({cfg.small_blind}/{cfg.big_blind})"
  )
  if cfg.timestamp is not None:
    top_line += f" - {cfg.timestamp.strftime('%Y/%m/%d %H:%M:%S ET')}"
  lines.append(top_line)
  # Note: some form of currency must be included for some software to work
  # correctly. Its absence can manifest in unexpected behavior such as seats
  # being out of order.
  second_line = f"Table '{cfg.table_name}' {cfg.seats}-max (USD)"
  button_display_number = (
      hand.button_index + 1 if hand.button_index is not None else cfg.seats
  )
  second_line += f" Seat #{button_display_number} is the button"
  lines.append(second_line)

  for p in hand.players:
    lines.append(
        f"Seat {p.seat + 1}: {p.id} ({cfg.starting_stacks[p.seat]} in chips)"
    )

  bb_idx = -1
  for e in hand.events:
    if e.kind == ActionKind.BB:
      bb_idx = e.actor
      break
  # Check if the hand is a preflop fold around. In this case, the expected
  # output is that the big blind is returned the difference between the big
  # blind and the small blind, and they collect 2x the small blind from the
  # pot. Not all visualizers enforce this behavior, but PokerTracker4 fails to
  # parse the hand history otherwise.
  is_preflop_fold_around = True
  for e in hand.events:
    if e.kind not in (
        ActionKind.SB,
        ActionKind.BB,
        ActionKind.ANTE,
        ActionKind.FOLD,
    ):
      is_preflop_fold_around = False
      break
  is_preflop_fold_around = (
      is_preflop_fold_around
      and bb_idx != -1
      and hand.summary_folded.count(False) == 1
      and not hand.summary_folded[bb_idx]
  )
  pfa_uncalled_amount = 0
  if is_preflop_fold_around:
    pfa_uncalled_amount = cfg.big_blind - cfg.small_blind

  # Blinds/Antes
  for event in [e for e in hand.events if e.street == Street.BLINDS]:
    lines.append(event.ps_text(hand.players[event.actor].id))

  # Hole cards
  lines.append("*** HOLE CARDS ***")
  for p, (c1, c2) in zip(hand.players, hand.hole_cards):
    if observer_id is None or p.id == observer_id:
      lines.append(f"Dealt to {p.id} [{c1} {c2}]")
    else:
      lines.append(f"Dealt to {p.id} [?? ??]")

  # Preflop
  for event in [e for e in hand.events if e.street == Street.PREFLOP]:
    lines.append(event.ps_text(hand.players[event.actor].id))

  # Flop, turn, river
  # Example street lines:
  # *** FLOP *** [As 5c Js]
  # *** TURN *** [As 5c Js] [Ac]
  # *** RIVER *** [As 5c Js] [Ac] [Ah]
  comm_accum: list[Card] = []
  board_cards_by_street: list[list[Card]] = []
  for st, name in [
      (Street.FLOP, "FLOP"),
      (Street.TURN, "TURN"),
      (Street.RIVER, "RIVER"),
  ]:
    idx = {Street.FLOP: 0, Street.TURN: 1, Street.RIVER: 2}[st]
    street_cards = hand.community[idx] if idx < len(hand.community) else []
    if street_cards:
      comm_accum.extend(street_cards)
      board_cards_by_street.append(street_cards)
      if st == Street.FLOP:
        board_txt = (
            "[" + " ".join(str(c) for c in board_cards_by_street[0]) + "]"
        )
      else:
        board_txt = " ".join(
            "[" + " ".join(str(c) for c in cards) + "]"
            for cards in board_cards_by_street
        )
      lines.append(f"*** {name} *** {board_txt}")
      for event in [e for e in hand.events if e.street == st]:
        lines.append(event.ps_text(hand.players[event.actor].id))

  hand_is_over = bool(hand.profits)
  if is_preflop_fold_around:
    if pfa_uncalled_amount > 0:
      receiver = hand.players[bb_idx]
      lines.append(
          f"Uncalled bet ({pfa_uncalled_amount}) returned to {receiver.id}"
      )
  elif (
      hand_is_over
      and hand.uncalled_amount > 0
      and hand.uncalled_receiver is not None
  ):
    receiver = hand.players[hand.uncalled_receiver]
    lines.append(
        f"Uncalled bet ({hand.uncalled_amount}) returned to {receiver.id}"
    )

  if not hand.profits:
    return "\n".join(lines)

  # Showdown decision (if all 5 board cards dealt and last action is check/call)
  river_events = [e for e in hand.events if e.street == Street.RIVER]
  last_river_action_is_passive = river_events and river_events[-1].kind in (
      ActionKind.CALL, ActionKind.CHECK)
  saw_showdown = bool(len(comm_accum) == 5 and last_river_action_is_passive)
  if saw_showdown:
    lines.append("*** SHOWDOWN ***")
    for wi in hand.winners:
      (c1, c2) = hand.hole_cards[wi]
      lines.append(f"{hand.players[wi].id}: shows [{c1} {c2}]")

  # Pot computation (total contributions minus uncalled), winners collection
  # Rebuild total contributions from events
  contrib_for_pot = [0] * cfg.seats
  street_contrib = [0] * cfg.seats
  current_street = Street.BLINDS
  for event in hand.events:
    if event.street != current_street:
      if not (
          current_street == Street.BLINDS and event.street == Street.PREFLOP
      ):
        street_contrib = [0] * cfg.seats
      current_street = event.street

    if event.kind in (
        ActionKind.SB,
        ActionKind.BB,
        ActionKind.ANTE,
    ):
      contrib_for_pot[event.actor] += event.delta
      street_contrib[event.actor] += event.delta
    elif event.kind == ActionKind.CALL:
      contrib_for_pot[event.actor] += event.delta
      street_contrib[event.actor] += event.delta
    elif event.kind == ActionKind.BET:
      contrib_for_pot[event.actor] += event.delta
      street_contrib[event.actor] += event.delta
    elif event.kind == ActionKind.RAISE:
      chips_this_action = event.to_amount - street_contrib[event.actor]
      contrib_for_pot[event.actor] += chips_this_action
      street_contrib[event.actor] += chips_this_action

  if is_preflop_fold_around:
    if pfa_uncalled_amount > 0:
      contrib_for_pot[bb_idx] -= pfa_uncalled_amount
  elif hand.uncalled_amount > 0 and hand.uncalled_receiver is not None:
    contrib_for_pot[hand.uncalled_receiver] -= hand.uncalled_amount
  total_pot = sum(contrib_for_pot)

  # Distribute winnings
  if hand.winners:
    share = total_pot / len(hand.winners)
    for winner in hand.winners:
      lines.append(f"{hand.players[winner].id} collected {share} from pot")
  else:
    # legacy edge case: SB/BB chop when both are winners implicitly
    if cfg.seats >= 2:
      lines.append(f"{hand.players[0].id} collected {total_pot/2} from pot")
      lines.append(f"{hand.players[1].id} collected {total_pot/2} from pot")

  # Summary
  lines.append("*** SUMMARY ***")
  lines.append(f"Total pot {total_pot} | Rake 0")
  if comm_accum:
    lines.append("Board [" + " ".join(str(c) for c in comm_accum) + "]")

  # Seat lines: show/fold
  if saw_showdown:
    for p in hand.players:
      idx = p.seat
      (c1, c2) = hand.hole_cards[idx]
      outcome = (
          "won ({})".format(total_pot / len(hand.winners))
          if hand.profits[idx] > 0
          else "lost"
      )
      lines.append(f"Seat {idx+1}: {p.id} showed [{c1} {c2}] and {outcome}")
  else:
    for p in hand.players:
      if hand.summary_folded[p.seat]:
        lines.append(f"Seat {p.seat+1}: {p.id} folded")

  return "\n".join(lines)

