
def recalculate_probabilities(state, assumed_deck, prize_guaranteed_counts):
    if not assumed_deck:
        return

    total_cards = sum(assumed_deck.values())
    known_total = sum(state.known_in_hand.values()) + sum(state.known_in_play.values()) + sum(state.known_in_discard.values())
    cards_unseen = max(0, total_cards - known_total)

    locked_prizes_count = sum(prize_guaranteed_counts.values())
    effective_prize_size = max(0, state.prize_size - locked_prizes_count)
    for card_id, total_count in assumed_deck.items():
        known = (state.known_in_hand.get(card_id, 0) +
                 state.known_in_play.get(card_id, 0) +
                 state.known_in_discard.get(card_id, 0))

        remaining = max(0, total_count - known)

        if cards_unseen > 0:
            if state.known_in_hand.get(card_id, 0) > 0:
                state.hand_probabilities[card_id] = 1.0
            else:
                n_draws = max(0, state.hand_size - sum(state.known_in_hand.values()))
                state.hand_probabilities[card_id] = hypergeometric_prob(cards_unseen, remaining, n_draws)

            state.deck_probabilities[card_id] = hypergeometric_prob(cards_unseen, remaining, state.deck_size)
            if card_id not in prize_guaranteed_counts:
                state.prize_probabilities[card_id] = hypergeometric_prob(cards_unseen, remaining, effective_prize_size)
        else:
            state.hand_probabilities[card_id] = 0.0
            state.deck_probabilities[card_id] = 0.0
            if card_id not in prize_guaranteed_counts:
                state.prize_probabilities[card_id] = 0.0


def recalculate_probabilities(state, assumed_deck, prize_guaranteed_counts):
    if not assumed_deck:
        return

    total_cards = sum(assumed_deck.values())
    known_total = sum(state.known_in_hand.values()) + sum(state.known_in_play.values()) + sum(state.known_in_discard.values())
    cards_unseen = max(0, total_cards - known_total)

    locked_prizes_count = sum(prize_guaranteed_counts.values())
    effective_prize_size = max(0, state.prize_size - locked_prizes_count)
    for card_id, total_count in assumed_deck.items():
        known = (state.known_in_hand.get(card_id, 0) +
                 state.known_in_play.get(card_id, 0) +
                 state.known_in_discard.get(card_id, 0))

        remaining = max(0, total_count - known)

        if cards_unseen > 0:
            if state.known_in_hand.get(card_id, 0) > 0:
                state.hand_probabilities[card_id] = 1.0
            else:
                n_draws = max(0, state.hand_size - sum(state.known_in_hand.values()))
                state.hand_probabilities[card_id] = hypergeometric_prob(cards_unseen, remaining, n_draws)

            state.deck_probabilities[card_id] = hypergeometric_prob(cards_unseen, remaining, state.deck_size)
            if card_id not in prize_guaranteed_counts:
                state.prize_probabilities[card_id] = hypergeometric_prob(cards_unseen, remaining, effective_prize_size)
        else:
            state.hand_probabilities[card_id] = 0.0
            state.deck_probabilities[card_id] = 0.0
            if card_id not in prize_guaranteed_counts:
                state.prize_probabilities[card_id] = 0.0


def recalculate_probabilities(state, assumed_deck, prize_guaranteed_counts):
    if not assumed_deck:
        return

    total_cards = sum(assumed_deck.values())
    known_total = sum(state.known_in_hand.values()) + sum(state.known_in_play.values()) + sum(state.known_in_discard.values())
    cards_unseen = max(0, total_cards - known_total)

    locked_prizes_count = sum(prize_guaranteed_counts.values())
    effective_prize_size = max(0, state.prize_size - locked_prizes_count)
    for card_id, total_count in assumed_deck.items():
        known = (state.known_in_hand.get(card_id, 0) +
                 state.known_in_play.get(card_id, 0) +
                 state.known_in_discard.get(card_id, 0))

        remaining = max(0, total_count - known)

        if cards_unseen > 0:
            if state.known_in_hand.get(card_id, 0) > 0:
                state.hand_probabilities[card_id] = 1.0
            else:
                n_draws = max(0, state.hand_size - sum(state.known_in_hand.values()))
                state.hand_probabilities[card_id] = hypergeometric_prob(cards_unseen, remaining, n_draws)

            state.deck_probabilities[card_id] = hypergeometric_prob(cards_unseen, remaining, state.deck_size)
            if card_id not in prize_guaranteed_counts:
                state.prize_probabilities[card_id] = hypergeometric_prob(cards_unseen, remaining, effective_prize_size)
        else:
            state.hand_probabilities[card_id] = 0.0
            state.deck_probabilities[card_id] = 0.0
            if card_id not in prize_guaranteed_counts:
                state.prize_probabilities[card_id] = 0.0

