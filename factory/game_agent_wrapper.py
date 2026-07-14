import importlib.util
import logging
from pathlib import Path
from cb_agents.orchestrator import Orchestrator
from factory.game_adapter import run_agent_turn

logger = logging.getLogger(__name__)

class CABTAgentWrapper:
    def __init__(self, agent_id: str, skills_dir: str, deck: list[int], g_logger, staging_dir: str = "staging", use_staging: bool = False, model_path: str = None):
        self.agent_id = agent_id
        self.skills_dir = Path(skills_dir)
        self.staging_dir = Path(staging_dir)
        self.deck = deck
        self.use_staging = use_staging
        self.g_logger = g_logger

        s_dir = self.staging_dir if (self.use_staging and ((self.staging_dir / "priority_rules.json").exists() or (self.staging_dir / "strategy_profiles.json").exists())) else self.skills_dir

        self.orchestrator = Orchestrator(log_dir=f"logs/{agent_id}", skills_dir=str(s_dir), model_path=model_path)
        self.orchestrator.start_game()
        self.g_logger.register_with_bus(self.orchestrator.bus)

        if self.use_staging:
            self._inject_staging_modules()

    def _inject_staging_modules(self):
        for name in ["hand_analyst", "turn_planner", "strategy_agent", "opponent_model"]:
            staging_file = self.staging_dir / f"{name}.py"
            if staging_file.exists():
                try:
                    spec = importlib.util.spec_from_file_location(f"staging_{name}", str(staging_file))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    class_name = "".join([part.capitalize() for part in name.split("_")])
                    cls = getattr(module, class_name)
                    
                    obj = cls(log_dir=str(self.orchestrator.log_dir), skills_dir=str(self.orchestrator.skills_dir))
                    if name == "hand_analyst":
                        self.orchestrator.hand_analyst = obj
                        self.orchestrator.bus.register_agent("hand_analyst", obj.receive)
                    elif name == "turn_planner":
                        self.orchestrator.turn_planner = obj
                        self.orchestrator.bus.register_agent("turn_planner", obj.receive)
                    elif name == "strategy_agent":
                        self.orchestrator.strategy_agent = obj
                        self.orchestrator.bus.register_agent("strategy_agent", obj.receive)
                    elif name == "opponent_model":
                        self.orchestrator.opponent_model = obj
                        self.orchestrator.bus.register_agent("opponent_model", obj.receive, perspective_flag="opponent")
                    logger.info(f"Successfully injected staging class for {name}")
                except Exception as e:
                    logger.error(f"Failed to inject staging class for {name}: {e}")

    def __call__(self, obs: dict, conf: dict = None) -> list[int]:
        selected = run_agent_turn(self.orchestrator, obs, self.deck)
        current_turn = obs.get("turn_number", 1)
        try:
            strategy_active = getattr(self.orchestrator.strategy_agent, "current_posture", "tempo")
            last_triggered = getattr(self.orchestrator.strategy_agent, "last_triggered_turn", 0)
            hand_score = getattr(self.orchestrator.hand_analyst, "last_hand_score", 5.0)
            opp_confidence = getattr(self.orchestrator.opponent_model, "archetype_confidence", 0.5)
            self.g_logger.log_reasoning(
                turn=current_turn,
                strategy_active=strategy_active,
                hand_score=hand_score,
                strategy_switch_considered=(last_triggered == current_turn),
                opponent_archetype_confidence=opp_confidence,
                reasoning_chain=f"Step choice executed. Strategy: {strategy_active}",
                reasoning_fired=True,
                reasoning_outcome="positive"
            )
        except Exception as e:
            logger.error(f"Failed to log reasoning: {e}")

        try:
            for log_entry in obs.get("logs", []):
                if log_entry.get("type") in (6, "coin_flip"):
                    self.g_logger.log_variance(
                        turn=current_turn,
                        event_type="coin_flip",
                        expected_outcome="heads",
                        actual_outcome=log_entry.get("result", "heads"),
                        impact_score=0.0
                    )
        except Exception as e:
            logger.error(f"Failed to log variance: {e}")

        return selected
