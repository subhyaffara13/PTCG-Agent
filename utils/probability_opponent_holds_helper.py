
def probability_opponent_holds_helper(
    card_name: str, 
    assumed_deck: Dict[int, int], 
    deck_size: int, 
    hand_size: int, 
    known_in_play: Dict[int, int], 
    known_in_discard: Dict[int, int]
) -> float:
    from cb_agents.card_registry import CardRegistry
    registry = CardRegistry()
    
    target_ids = []
    for cid in assumed_deck.keys():
        try:
            card = registry.get_full_skill(cid)
            if card and card.name.lower() == card_name.lower().replace("'", "").replace("’", ""):
                target_ids.append(cid)
        except:
            pass
            
    if not target_ids:
        return 0.0
        
    N = deck_size + hand_size
    H = hand_size
    if N <= 0 or H <= 0:
        return 0.0
        
    D = 0
    for cid in target_ids:
        played = known_in_play.get(cid, 0) + known_in_discard.get(cid, 0)
        D += max(0, assumed_deck.get(cid, 0) - played)
        
    if D <= 0:
        return 0.0
        
    if N - D < H:
        return 1.0
        
    try:
        prob_none = math.comb(N - D, H) / math.comb(N, H)
        return 1.0 - prob_none
    except (ValueError, ZeroDivisionError):
        return 0.0


def probability_opponent_holds_helper(
    card_name: str, 
    assumed_deck: Dict[int, int], 
    deck_size: int, 
    hand_size: int, 
    known_in_play: Dict[int, int], 
    known_in_discard: Dict[int, int],
    known_in_hand: Dict[int, int] | None = None,
    prize_size: int = 6
) -> float:
    registry = _get_registry()
    
    target_ids = []
    for cid in assumed_deck.keys():
        try:
            card = registry.get_full_skill(cid)
            cname = getattr(card, "card_name", "") if card else ""
            if cname and cname.lower() == card_name.lower().replace("'", "").replace("’", ""):
                target_ids.append(cid)
        except Exception as e:
            logger.debug(f"Opponent holds card match failed for ID {cid}: {e}")
            
    if not target_ids:
        return 0.0

    if known_in_hand:
        for cid in target_ids:
            if known_in_hand.get(cid, 0) > 0:
                return 1.0
    
    # Total unseen pool: deck + hand + prizes (all cards not yet in play/discard)
    N = deck_size + hand_size + max(0, prize_size)
    H = hand_size
    if N <= 0 or H <= 0:
        return 0.0
        
    D = 0
    for cid in target_ids:
        played = known_in_play.get(cid, 0) + known_in_discard.get(cid, 0) + (known_in_hand.get(cid, 0) if known_in_hand else 0)
        D += max(0, assumed_deck.get(cid, 0) - played)
        
    if D <= 0:
        return 0.0
        
    if N - D < H:
        return 1.0
        
    try:
        prob_none = math.comb(N - D, H) / math.comb(N, H)
        base_prob = 1.0 - prob_none
        # Adjust for hand size density: larger hands increase likelihood of holding key responses
        if H >= 6:
            base_prob = min(1.0, base_prob * 1.15)
        return base_prob
    except (ValueError, ZeroDivisionError):
        return 0.0


def probability_opponent_holds_helper(
    card_name: str, 
    assumed_deck: Dict[int, int], 
    deck_size: int, 
    hand_size: int, 
    known_in_play: Dict[int, int], 
    known_in_discard: Dict[int, int],
    known_in_hand: Dict[int, int] | None = None,
    prize_size: int = 6
) -> float:
    registry = _get_registry()
    
    target_ids = []
    for cid in assumed_deck.keys():
        try:
            card = registry.get_full_skill(cid)
            cname = getattr(card, "card_name", "") if card else ""
            if cname and cname.lower() == card_name.lower().replace("'", "").replace("’", ""):
                target_ids.append(cid)
        except Exception as e:
            logger.debug(f"Opponent holds card match failed for ID {cid}: {e}")
            
    if not target_ids:
        return 0.0

    if known_in_hand:
        for cid in target_ids:
            if known_in_hand.get(cid, 0) > 0:
                return 1.0
    
    # Total unseen pool: deck + hand + prizes (all cards not yet in play/discard)
    N = deck_size + hand_size + max(0, prize_size)
    H = hand_size
    if N <= 0 or H <= 0:
        return 0.0
        
    D = 0
    for cid in target_ids:
        played = known_in_play.get(cid, 0) + known_in_discard.get(cid, 0) + (known_in_hand.get(cid, 0) if known_in_hand else 0)
        D += max(0, assumed_deck.get(cid, 0) - played)
        
    if D <= 0:
        return 0.0
        
    if N - D < H:
        return 1.0
        
    try:
        prob_none = math.comb(N - D, H) / math.comb(N, H)
        base_prob = 1.0 - prob_none
        # Adjust for hand size density: larger hands increase likelihood of holding key responses
        if H >= 6:
            base_prob = min(1.0, base_prob * 1.15)
        return base_prob
    except (ValueError, ZeroDivisionError):
        return 0.0

