from typing import List, Dict, Any

class HandHelpersMixin:
    def has_tag(self, tags, name: str, bit: int) -> bool:
        if hasattr(tags, "value"):
            return bool(tags.value & bit)
        if isinstance(tags, (list, tuple)):
            return name in tags
        if isinstance(tags, str):
            return name.lower() in tags.lower()
        return False

    def eval_hand_cards(self, hand: List[str], registry: Any):
        ev_scores, hand_cards_data = [], []
        flags = {
            "has_basic": False, "has_energy": False, "has_supporter": False,
            "has_search": False, "has_draw": False, "has_discard": False,
            "has_rare_candy": False, "supporter_count": 0, "stage1_count": 0, "stage2_count": 0
        }

        for cid in hand:
            card = registry.get_full_skill(cid)
            if card:
                ev_score = getattr(card, "ev_score", 0.1)
                ctype = getattr(card, "card_type", "Trainer")
                tags = getattr(card, "combo_tags", [])
                
                if ctype == "Pokemon" or (hasattr(ctype, "name") and ctype.name == "POKEMON"):
                    if self.has_tag(tags, "Basic", 4096): flags["has_basic"] = True
                    if self.has_tag(tags, "Stage 1", 16384): flags["stage1_count"] += 1
                    if self.has_tag(tags, "Stage 2", 32768): flags["stage2_count"] += 1
                elif ctype == "Trainer" or (hasattr(ctype, "name") and ctype.name == "TRAINER"):
                    if self.has_tag(tags, "Supporter", 8192):
                        flags["has_supporter"] = True
                        flags["supporter_count"] += 1
                    if self.has_tag(tags, "search", 1): flags["has_search"] = True
                    if self.has_tag(tags, "draw", 8): flags["has_draw"] = True
                    if self.has_tag(tags, "discard", 128): flags["has_discard"] = True
                    if "rare candy" in str(getattr(card, "card_name", "")).lower():
                        flags["has_rare_candy"] = True
                elif ctype == "Energy" or (hasattr(ctype, "name") and ctype.name == "ENERGY"):
                    flags["has_energy"] = True
                    ev_score += 0.05
                hand_cards_data.append((card, ev_score))
            else:
                ev_score = 0.1
                hand_cards_data.append(({"card_id": cid, "card_name": cid, "card_type": "Trainer"}, ev_score))
            ev_scores.append(ev_score)
        return ev_scores, hand_cards_data, flags

    def get_multipliers_and_bonuses(self, flags, strategy_tips, cfg, supporter_count):
        multiplier = 1.0
        if flags["has_search"] and flags["has_basic"]: multiplier += cfg["search_bench_mult"]
        if flags["has_discard"] and flags["has_draw"]: multiplier += cfg["discard_draw_mult"]
        if flags["has_discard"] and flags["has_search"] and flags["has_energy"]: multiplier += cfg["discard_search_energy_mult"]
        if flags["has_rare_candy"] and flags["stage2_count"] > 0: multiplier += cfg["rare_candy_stage2_mult"]
        if flags["has_draw"] and strategy_tips.get("priority_modifiers", {}).get("force_draw_engine"):
            multiplier *= float(strategy_tips["priority_modifiers"]["force_draw_engine"])
        
        bonus = 0.0
        if supporter_count > cfg["supp_thresh"]:
            bonus -= cfg["supp_factor"] * (supporter_count - 1)
        return multiplier, bonus

    def eval_bricks_evo(self, hand: List[str], board: List[str], registry: Any, cfg: dict):
        brick_count = evolution_matches = 0
        available_names = {str(getattr(registry.get_full_skill(cid), "card_name", "")).lower() for cid in hand + board if registry.get_full_skill(cid)}
        for cid in hand:
            card = registry.get_full_skill(cid)
            if card and (getattr(card, "card_type", "") == "Pokemon" or getattr(getattr(card, "card_type", None), "name", "") == "POKEMON"):
                tags = getattr(card, "combo_tags", [])
                if self.has_tag(tags, "Stage 1", 16384) or self.has_tag(tags, "Stage 2", 32768):
                    predecessor = registry.get_evolution_predecessor(str(getattr(card, "card_name", "")).lower())
                    if predecessor and predecessor in available_names:
                        evolution_matches += 1
                    else:
                        brick_count += 1
        return -(brick_count * cfg["brick_factor"]), (evolution_matches * cfg["evo_match_factor"])

    def apply_phase_bonuses(self, phase: str, flags, hand_cards_data, cfg: dict):
        bonus = 0.0
        if phase == 'early':
            if flags["has_basic"]: bonus += cfg["early_basic_bonus"]
            if flags["has_supporter"]: bonus += cfg["early_supporter_bonus"]
        elif phase == 'mid':
            if flags["has_energy"]: bonus += cfg["mid_energy_bonus"]
            if any(getattr(c[0], "card_type", "") == "Pokemon" and "Stage" in getattr(c[0], "card_name", "") for c in hand_cards_data):
                bonus += cfg["mid_evolution_bonus"]
        else:
            has_late_attacker = any(getattr(c[0], "damage_output", 0) > 0 for c in hand_cards_data if getattr(c[0], "card_type", "") == "Pokemon" or getattr(getattr(c[0], "card_type", None), "name", "") == "POKEMON")
            if has_late_attacker: bonus += cfg["late_attacker_bonus"]
            if any(c[1] > cfg["late_high_ev_threshold"] for c in hand_cards_data): bonus += cfg["late_high_ev_bonus"]
        return bonus
