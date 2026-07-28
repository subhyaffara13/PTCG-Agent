from typing import List, Dict

class SequencingEngine:
    PHASE_ORDER = ["zero_cost_draw", "search", "draw", "board", "attack"]
    
    def get_phase(self, action: str) -> str:
        # Zero-cost draw abilities (Concealed Cards, Refinement, Trade) run BEFORE deck search!
        if action.startswith("ability:"):
            target = action.split(":", 1)[1].lower()
            if any(dk in target for dk in ("concealed", "refinement", "trade", "shining arcana", "draw")):
                return "zero_cost_draw"
        if action.startswith("play_trainer:"):
            action_suffix = action[13:].replace("_", " ").replace("'", "").lower()
            from cb_agents.card_registry import CardRegistry
            from cb_agents.card_types import ComboTag
            registry = CardRegistry()
            for card in registry.cards.values():
                c_name = card.card_name.replace("'", "").lower()
                if c_name == action_suffix or action_suffix in c_name:
                    try:
                        heavy = registry.get_full_skill(card.card_id)
                    except Exception as e:
                        import logging
                        logging.error(f"get_full_skill failed: {e}")
                        continue
                    if heavy:
                        if heavy.combo_tags & ComboTag.SEARCH:
                            return "search"
                        if heavy.combo_tags & ComboTag.DRAW:
                            return "draw"
                    break
        elif action.startswith("attack:") or action == "pass":
            return "attack"
        return "board"
        
    def group_actions(self, legal_actions: List[str]) -> Dict[str, List[str]]:
        groups = {phase: [] for phase in self.PHASE_ORDER}
        for action in legal_actions:
            phase = self.get_phase(action)
            groups[phase].append(action)
        return groups
        
    def sequence_actions(self, legal_actions: List[str], game_state) -> List[str]:
        groups = self.group_actions(legal_actions)
        prioritized = []
        for phase in self.PHASE_ORDER:
            prioritized.extend(groups[phase])
        return prioritized
