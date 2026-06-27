from typing import List, Dict

class SequencingEngine:
    PHASE_ORDER = ["search", "draw", "board", "attack"]
    
    def get_phase(self, action: str) -> str:
        if action.startswith("play_trainer:"):
            action_suffix = action[13:].replace("_", " ").replace("'", "").lower()
            from agents.card_registry import CardRegistry
            from agents.card_types import ComboTag
            registry = CardRegistry()
            for card in registry.cards.values():
                c_name = card.card_name.replace("'", "").lower()
                if c_name == action_suffix or action_suffix in c_name:
                    heavy = registry.get_full_skill(card.card_id)
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
