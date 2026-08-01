
def _card_suit_rank(card_str: str) -> tuple[str, str]:
    """Parse OpenSpiel card label like '♣10' or '♥A' into (suit, rank).

    Normalizes rank "10" to "T" so the canonical form is one char and
    sortable via ``_RANK_ORDER``.
    """
    suit = card_str[0]
    rank = card_str[1:]
    if rank == "10":
        rank = "T"
    return suit, rank

