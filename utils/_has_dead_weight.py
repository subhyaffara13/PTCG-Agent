
def _has_dead_weight(game_state: dict) -> bool:
    hand = game_state.get("my_hand", [])
    if not isinstance(hand, list) or len(hand) < 4:
        return False
    try:
        supporter_names = []
        basic_energy_count = 0
        stage2_count = 0
        for cid_str in hand:
            try:
                card = _registry.get(int(cid_str))
                if card:
                    if card.card_type.name == "TRAINER" and getattr(card, "trainer_subtype", None) and card.trainer_subtype.name == "SUPPORTER":
                        supporter_names.append(card.card_name)
                    if card.card_type.name == "ENERGY":
                        basic_energy_count += 1
                    if card.stage and card.stage == CardStage.STAGE2:
                        stage2_count += 1
            except:
                pass
        dup_supporters = len(supporter_names) - len(set(supporter_names))
        return dup_supporters >= 2 or basic_energy_count >= 6 or stage2_count >= 2
    except ImportError:
        return len(hand) >= 7

