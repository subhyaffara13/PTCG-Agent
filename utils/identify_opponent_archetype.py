
def identify_opponent_archetype(revealed_state: List[Any], archetypes: Dict[str, Any]) -> tuple[str, float]:
    """Identifies archetype and returns (archetype_name, confidence)."""
    # 1. Fast ID check
    for card in revealed_state:
        if str(card) in KEY_ID_TO_ARCHETYPE:
            return KEY_ID_TO_ARCHETYPE[str(card)], 0.99
            
    total_revealed = len(revealed_state)
    if total_revealed < 1 or not archetypes:
        return "unknown", 0.0

    # Pre-compute card identifiers for all revealed cards once
    revealed_idents = [(str(c).lower().replace(" ", "-"), get_card_identifier(c)) for c in revealed_state]

    best_score = 0.0
    best_archetype = "unknown"
    has_sig_match = False
    
    for arch_name, arch_data in archetypes.items():
        signature_cards = [sig.lower().replace(" ", "-") for sig in arch_data.get("signature_cards", [])]
        card_pool = [cp.lower().replace(" ", "-") for cp in arch_data.get("card_pool", [])]
        
        score = 0.0
        arch_has_sig = False
        for raw_str, ident in revealed_idents:
            is_sig = (raw_str in signature_cards) or any((len(ident) > 4 and (ident in sig or sig in ident)) for sig in signature_cards)
            if is_sig:
                score += 2.0
                arch_has_sig = True
                continue
            is_pool = (raw_str in card_pool) or any((len(ident) > 4 and (ident in cp or cp in ident)) for cp in card_pool)
            if is_pool:
                score += 1.0
                
        if score > best_score:
            best_score = score
            best_archetype = arch_name
            has_sig_match = arch_has_sig
            
    if best_score > 0.0:
        if has_sig_match:
            confidence = min(0.95, 0.80 + (best_score * 0.05))
        else:
            confidence = round(best_score / (total_revealed * 2.0), 4) if total_revealed >= 3 else 0.0
        return best_archetype, confidence
        
    return "unknown", 0.0


def identify_opponent_archetype(revealed_state: List[Any], archetypes: Dict[str, Any]) -> tuple[str, float]:
    """Identifies archetype and returns (archetype_name, confidence)."""
    # 1. Fast ID check
    for card in revealed_state:
        if str(card) in KEY_ID_TO_ARCHETYPE:
            return KEY_ID_TO_ARCHETYPE[str(card)], 0.99
            
    total_revealed = len(revealed_state)
    if total_revealed < 1 or not archetypes:
        return "unknown", 0.0

    # Pre-compute card identifiers for all revealed cards once
    revealed_idents = [(str(c).lower().replace(" ", "-"), get_card_identifier(c)) for c in revealed_state]

    best_score = 0.0
    best_archetype = "unknown"
    has_sig_match = False
    
    for arch_name, arch_data in archetypes.items():
        signature_cards = [sig.lower().replace(" ", "-") for sig in arch_data.get("signature_cards", [])]
        card_pool = [cp.lower().replace(" ", "-") for cp in arch_data.get("card_pool", [])]
        
        score = 0.0
        arch_has_sig = False
        for raw_str, ident in revealed_idents:
            is_sig = (raw_str in signature_cards) or any((len(ident) > 4 and (ident in sig or sig in ident)) for sig in signature_cards)
            if is_sig:
                score += 2.0
                arch_has_sig = True
                continue
            is_pool = (raw_str in card_pool) or any((len(ident) > 4 and (ident in cp or cp in ident)) for cp in card_pool)
            if is_pool:
                score += 1.0
                
        if score > best_score:
            best_score = score
            best_archetype = arch_name
            has_sig_match = arch_has_sig
            
    if best_score > 0.0:
        if has_sig_match:
            confidence = min(0.95, 0.80 + (best_score * 0.05))
        else:
            confidence = round(best_score / (total_revealed * 2.0), 4) if total_revealed >= 3 else 0.0
        return best_archetype, confidence
        
    return "unknown", 0.0


def identify_opponent_archetype(revealed_state: List[Any], archetypes: Dict[str, Any]) -> tuple[str, float]:
    """Identifies archetype and returns (archetype_name, confidence)."""
    # 1. Fast ID check
    for card in revealed_state:
        if str(card) in KEY_ID_TO_ARCHETYPE:
            return KEY_ID_TO_ARCHETYPE[str(card)], 0.99
            
    total_revealed = len(revealed_state)
    if total_revealed < 3 or not archetypes:
        return "unknown", 0.0

    best_match_count = 0
    best_archetype = "unknown"
    
    for arch_name, arch_data in archetypes.items():
        signature_cards = set(arch_data.get("signature_cards", []))
        card_pool = set(arch_data.get("card_pool", []))
        
        matches = sum(1 for c in revealed_state if c in signature_cards or c in card_pool)
        if matches > best_match_count:
            best_match_count = matches
            best_archetype = arch_name
            
    if best_match_count > 0:
        return best_archetype, round(best_match_count / total_revealed, 4)
        
    return "unknown", 0.0

