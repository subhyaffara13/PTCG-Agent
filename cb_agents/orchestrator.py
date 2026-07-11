"""agents/orchestrator.py -- Thin shell that owns Orchestrator.

Delegates step logic to orchestrator_steps.py and logging to orchestrator_log.py.
"""

from __future__ import annotations
from typing import Any
from pathlib import Path

import logging
from router.bus import RouterBus

logger = logging.getLogger(__name__)
from cb_agents.hand_analyst   import HandAnalyst
from cb_agents.turn_planner   import TurnPlanner
from cb_agents.time_manager   import TimeManager
from cb_agents.strategy_agent import StrategyAgent
from cb_agents.opponent_model import OpponentModel
from cb_agents.orchestrator_types import TurnDecision
from cb_agents.orchestrator_steps import _step_time, _step_hand, _step_plan, _step_strategy, _step_opponent
from cb_agents.orchestrator_merge import _merge, _emergency_pass
from cb_agents.orchestrator_log import _log_orchestration

from cb_agents.orchestrator_belief import OrchestratorBeliefMixin
from cb_agents.orchestrator_state_public import OrchestratorStatePublicMixin
from cb_agents.belief_tracker import BeliefTracker
from cb_agents.deck_loader import load_deck_base_list


import os
is_kaggle = any(k.startswith("KAGGLE") for k in os.environ) or not os.path.exists("build_submission.py")

class Orchestrator(OrchestratorBeliefMixin, OrchestratorStatePublicMixin):
    def __init__(self, **kwargs: Any) -> None:
        self.skills_dir = Path(kwargs.get("skills_dir")) if kwargs.get("skills_dir") else Path("skills")
        self.log_dir = Path(kwargs.get("log_dir")) if kwargs.get("log_dir") else Path("logs")
        
        # Initialize belief tracker with loaded base deck list
        initial_deck = load_deck_base_list(self.skills_dir)
        self.belief_tracker = BeliefTracker(initial_deck)
        
        delegation_map = {
            "TimeManager": "time_manager",
            "HandAnalyst": "hand_analyst",
            "TurnPlanner": "turn_planner",
            "StrategyAgent": "strategy_agent",
            "OpponentModel": "opponent_model"
        }
        self.bus = self._router = RouterBus(delegation_map=delegation_map, log_dir=str(self.log_dir))
        self.hand_analyst = self._analyst  = HandAnalyst(**kwargs)
        self.turn_planner = self._planner  = TurnPlanner(belief_tracker=self.belief_tracker, **kwargs)
        self.time_manager = self._timer    = TimeManager(**kwargs)
        self.strategy_agent = self._strategy = StrategyAgent(**kwargs)
        self.opponent_model = self._opponent = OpponentModel(**kwargs)
        self.context   = {}
        for agent in (self.hand_analyst, self.turn_planner, self.time_manager, self.strategy_agent, self.opponent_model):
            agent.shared_context = self.context

        self.bus.register_agent("time_manager", self._timer.tick)
        self.bus.register_agent("hand_analyst", self._analyst.analyse)
        self.bus.register_agent("turn_planner", self._planner.receive)
        self.bus.register_agent("strategy_agent", self._strategy.evaluate)
        self.bus.register_agent("opponent_model", self._opponent.receive, perspective_flag="opponent")

    def orchestrate(self, game_state: dict[str, Any]) -> TurnDecision:
        time_result = _step_time(game_state, self._timer, self._router)
        if time_result.get("directive") == "FORCE_PASS":
            return _emergency_pass(time_result)
        try:
            hand_result  = _step_hand(game_state, self._analyst, self._router)
            # Store hand_score dynamically into game_state dict
            game_state["hand_score"] = hand_result.get("hand_score", 0.0)
            
            # Sync the belief tracker with the opponent's public state
            self.sync_belief_tracker(game_state)
            
            strat_result = _step_strategy(game_state, self, self._router)
            plan_result  = _step_plan(game_state, hand_result, strat_result, self._planner, self._router)
            opp_result   = _step_opponent(game_state, self._opponent, self._router)
            decision     = _merge(game_state, time_result, hand_result, plan_result, strat_result, opp_result)
            _log_orchestration(game_state, decision)
            return decision
        except Exception as e:
            logger.exception("CRITICAL: Exception in Orchestrator.orchestrate")
            import sys
            import subprocess
            import json
            sys.stderr.write(f"CRITICAL: Exception in Orchestrator.orchestrate: {e}\n")
            import traceback
            tb_str = traceback.format_exc()
            sys.stderr.write(tb_str + "\n")
            
            try:
                req_path = Path(self.log_dir) / "evolution_request.json"
                # Find which agent file caused the traceback
                target_file = "cb_agents/turn_planner_sort.py"
                for line in tb_str.splitlines():
                    if "agents/" in line or "cb_agents/" in line:
                        for filename in ("turn_planner_sort.py", "turn_planner_resolve.py", "turn_planner_heuristics.py", "orchestrator_belief.py", "hand_analyst_helpers.py"):
                            if filename in line:
                                target_file = f"cb_agents/{filename}"
                                break
                
                req_data = {
                    "file_to_mutate": target_file,
                    "exception": str(e),
                    "traceback": tb_str,
                    "game_turn": game_state.get("turn_number", 1)
                }
                req_path.parent.mkdir(parents=True, exist_ok=True)
                req_path.write_text(json.dumps(req_data, indent=2), encoding="utf-8")
                
                if os.environ.get("AUTO_EVOLVE") == "true" and not is_kaggle:
                    sys.stderr.write(f"AUTO_EVOLVE is active. Spawning code_mutator for {target_file}...\n")
                    subprocess.Popen(
                        [sys.executable, "-m", "cb_agents.code_mutator", target_file],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        close_fds=True
                    )
            except Exception as log_err:
                sys.stderr.write(f"Failed to log/trigger evolution request: {log_err}\n")
                
            try:
                legal = game_state.get("legal_actions", [])
                if legal:
                    return TurnDecision(
                        action_sequence=[legal[0]],
                        primary_action=legal[0],
                        reasoning_chain="emergency_fallback",
                        strategy_profile="aggro_push"
                    )
            except Exception as fallback_err:
                logger.exception(f"Emergency fallback failed: {fallback_err}")
            return _emergency_pass(time_result)

    def start_game(self) -> None:
        pass
        
    run_turn = orchestrate

    def flush_all_logs(self) -> None:
        try:
            self._timer.flush_logs()
        except Exception as e:
            logger.debug(f"Flush time manager logs failed: {e}")
        try:
            self._analyst.flush_logs()
        except Exception as e:
            logger.debug(f"Flush analyst logs failed: {e}")
        try:
            self._planner.flush_logs()
        except Exception as e:
            logger.debug(f"Flush planner logs failed: {e}")
        try:
            from cb_agents.strategy_agent_io import flush_logs as flush_strategy_logs
            flush_strategy_logs()
        except Exception as e:
            logger.debug(f"Flush strategy logs failed: {e}")
        try:
            from cb_agents.orchestrator_log import flush_logs as flush_orch_logs
            flush_orch_logs()
        except Exception as e:
            logger.debug(f"Flush orchestrator logs failed: {e}")
