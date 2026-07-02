import json
import logging
from pathlib import Path
from typing import Any, Dict
from agents.base_agent import BaseAgent
from router.bus import OpponentModelPacket
from agents.registry import register_agent
from agents.opponent_model_helpers import identify_opponent_archetype, predict_opponent_action

logger = logging.getLogger(__name__)
@register_agent("opponent_model", perspective_flag="opponent")
class OpponentModel(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", perspective_flag: str = "opponent", shared_context=None):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        self.shared_context = shared_context
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            self.skills_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.warning(f"Could not create opponent model directories: {e}")

        self.reasoning_log_file = self.log_dir / "opponent_model_reasoning.json"
        self._reasoning_buffer = []
        if self.shared_context:
            self.archetypes = self.shared_context.get_config(str(self.skills_dir), "deck_archetypes.json").get("archetypes", {})
        else:
            self.archetypes = self._load_deck_archetypes()
        self.revealed_state = []
        self.inferred_state = {}
        self.archetype_confidence = 0.0
        self.identified_archetype = "unknown"
        self.opponent_searched_last_turn = False

    def _load_deck_archetypes(self) -> dict:
        path = self.skills_dir / "deck_archetypes.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                return data.get("archetypes", {})
            except Exception as e:
                logger.error(f"Failed to read deck_archetypes.json: {e}")
        return {}

    def receive(self, packet: Any) -> dict:
        if hasattr(packet, "_asdict"): packet = packet._asdict()
        elif hasattr(packet, "__dict__"): packet = packet.__dict__
        if not isinstance(packet, dict):
            raise TypeError(f"OpponentModel received illegal packet type: {type(packet).__name__}.")

        revealed_cards = packet.get("revealed_cards") or packet.get("newly_played_cards", [])
        turn_number = packet.get("turn_number") or packet.get("turn", 1)
        prizes_remaining = packet.get("prizes_remaining") or packet.get("revealed_prizes_remaining", 6)

        for card in revealed_cards:
            if card not in self.revealed_state:
                self.revealed_state.append(card)

        # IDENTIFY ARCHETYPE
        self.identified_archetype, self.archetype_confidence = identify_opponent_archetype(
            self.revealed_state, self.archetypes
        )

        # FILL INFERRED STATE
        if self.identified_archetype != "unknown" and self.identified_archetype in self.archetypes:
            pool = self.archetypes[self.identified_archetype].get("card_pool", [])
            self.inferred_state = {c: 1.0 for c in pool if c not in self.revealed_state}
        else:
            self.inferred_state = {}

        # PREDICT ACTION
        predicted = predict_opponent_action(self.identified_archetype, prizes_remaining, turn_number)

        reasoning = f"Identified {self.identified_archetype} with {round(self.archetype_confidence * 100, 2)}% confidence. Predicting {predicted}."

        self._reasoning_buffer.append({
            "turn": turn_number,
            "perspective": self.perspective_flag,
            "revealed_count": len(self.revealed_state),
            "identified_archetype": self.identified_archetype,
            "confidence": self.archetype_confidence,
            "predicted_next_action": predicted,
            "reasoning": reasoning,
            "opponent_searched_last_turn": self.opponent_searched_last_turn
        })

        return {
            "predicted_next_action": predicted,
            "archetype_confidence": self.archetype_confidence,
            "inferred_deck_type": self.identified_archetype,
            "reasoning": reasoning,
            "opponent_searched_last_turn": self.opponent_searched_last_turn
        }
    def flush_logs(self):
        if not self._reasoning_buffer:
            return
        try:
            with open(self.reasoning_log_file, "a", encoding="utf-8") as f:
                for entry in self._reasoning_buffer:
                    f.write(json.dumps(entry) + "\n")
            self._reasoning_buffer.clear()
        except Exception as e:
            logger.error(f"Failed to flush opponent model reasoning logs: {e}")
