
def _synergy_score(card, core_elements, core_tags, details):
    base_ev = card.get("ev_score", 0.0)
    det = details.get(str(card["card_id"]), {}); synergy = 0.0
    if card.get("card_type") == "Pokemon" and core_elements:
        elem = det.get("element_type", "")
        if elem in core_elements or elem == "Colorless": synergy += 0.5
        else: synergy -= 0.5
    if set(card.get("combo_tags", [])) and core_tags and set(card.get("combo_tags", [])).intersection(core_tags):
        synergy += 0.2
    return base_ev + synergy

