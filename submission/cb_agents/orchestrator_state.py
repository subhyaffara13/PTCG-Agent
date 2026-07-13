import json
import logging
from cb_agents.registry import get_registered_agents

logger = logging.getLogger(__name__)

class OrchestratorStateMixin:
    def load_delegation_map(self) -> dict:
        path = self.skills_dir / "delegation_map.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                return data.get("delegation", {})
            except Exception as e:
                logger.warning(f"Delegation map parse failed: {e}")
        return {
            "turn_start": "hand_analyst",
            "after_hand_analysis": "turn_planner",
            "on_trigger": "strategy_agent",
            "on_opponent_play": "opponent_model",
            "before_turn_planner": "lethal_calculator",
            "always": "time_manager"
        }

    def initialize_and_register_agents(self):
        """Initializes and registers sub-agents on the bus."""
        for bus_name, meta in get_registered_agents().items():
            kwargs: dict = {"log_dir": str(self.log_dir)}
            if meta["needs_skills_dir"]:
                kwargs["skills_dir"] = str(self.skills_dir)
            if meta["needs_shared_context"]:
                kwargs["shared_context"] = self.context

            instance = meta["cls"](**kwargs)
            setattr(self, bus_name, instance)

            reg_kwargs: dict = {}
            if meta["perspective_flag"] != "player":
                reg_kwargs["perspective_flag"] = meta["perspective_flag"]
            self.bus.register_agent(bus_name, instance.receive, **reg_kwargs)
