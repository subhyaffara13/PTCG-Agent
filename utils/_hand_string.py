
def _hand_string(cards):
  """Returns the hand of the to-play player in the state in BlueChip format."""
  if len(cards) != 13:
    raise ValueError("Must have 13 cards")
  suits = [[] for _ in range(4)]
  for card in reversed(sorted(cards)):
    suit = card % 4
    rank = card // 4
    suits[suit].append(_RANKS[rank])
  for i in range(4):
    if suits[i]:
      suits[i] = _TRUMP_SUIT[i] + " " + " ".join(suits[i]) + "."
    else:
      suits[i] = _TRUMP_SUIT[i] + " -."
  return " ".join(suits)


def _hand_string(state_vec):
  """Returns the hand of the to-play player in the state in BlueChip format."""
  # See UncontestedBiddingState::InformationStateTensor
  # The first 52 elements are whether or not we hold the given card (cards
  # ordered suit-by-suit, in ascending order of rank).
  suits = []
  for suit in reversed(range(4)):
    cards = []
    for rank in reversed(range(13)):
      if state_vec[rank * 4 + suit]:
        cards.append(_RANKS[rank])
    suits.append(_TRUMP_SUIT[suit] + " " + (" ".join(cards) if cards else "-") +
                 ".")
  return " ".join(suits)

