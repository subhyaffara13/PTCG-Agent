
def _trick_winner_idx(trick_cards: list[str], trump: str | None) -> int:
    """Return the 0..3 index of the winning card in a 4-card trick.

    Trump cards beat non-trump; among trump (or among led suit if no
    trump played) highest rank wins. ``trump`` is a suit glyph
    (♣/♦/♥/♠) or ``None`` for no-trump contracts.
    """
    suit0, rank0 = _card_suit_rank(trick_cards[0])
    led_suit = suit0
    best_idx = 0
    best_rank = _RANK_ORDER.index(rank0)
    best_is_trump = trump is not None and suit0 == trump
    for i in range(1, len(trick_cards)):
        suit, rank = _card_suit_rank(trick_cards[i])
        rank_val = _RANK_ORDER.index(rank)
        is_trump = trump is not None and suit == trump
        if is_trump and (not best_is_trump or rank_val > best_rank):
            best_idx, best_rank, best_is_trump = i, rank_val, True
        elif not is_trump and not best_is_trump and suit == led_suit and rank_val > best_rank:
            best_idx, best_rank = i, rank_val
    return best_idx

