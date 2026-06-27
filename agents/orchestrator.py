"""agents/orchestrator.py -- Thin shell that owns Orchestrator.

Delegates step logic to orchestrator_steps.py and logging to orchestrator_log.py.
"""

from __future__ import annotations
from typing import Any

from router.bus import RouterBus
from agents.hand_analyst   import HandAnalyst
from agents.turn_planner   import TurnPlanner
from agents.time_manager   import TimeManager
from agents.strategy_agent import StrategyAgent
from agents.opponent_model import OpponentModel
from agents.orchestrator_types import TurnDecision
from agents.orchestrator_steps import (
    _step_time, _step_hand, _step_plan, _step_strategy, _step_opponent,
)
from agents.orchestrator_merge import _merge, _emergency_pass
from agents.orchestrator_log import _log_orchestration


class Orchestrator:
    def __init__(self, **kwargs: Any) -> None:
        delegation_map = {
            "TimeManager": "time_manager",
            "HandAnalyst": "hand_analyst",
            "TurnPlanner": "turn_planner",
            "StrategyAgent": "strategy_agent",
            "OpponentModel": "opponent_model"
        }
        self.bus = self._router = RouterBus(delegation_map=delegation_map, log_dir=kwargs.get("log_dir", "logs"))
        self.hand_analyst = self._analyst  = HandAnalyst(**kwargs)
        self.turn_planner = self._planner  = TurnPlanner(**kwargs)
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
        if time_result["directive"] == "FORCE_PASS":
            return _emergency_pass(time_result)
        hand_result  = _step_hand(game_state, self._analyst, self._router)
        plan_result  = _step_plan(hand_result, self._planner, self._router)
        strat_result = _step_strategy(game_state, self._strategy, self._router)
        opp_result   = _step_opponent(game_state, self._opponent, self._router)
        decision     = _merge(game_state, time_result, hand_result, plan_result, strat_result, opp_result)
        _log_orchestration(game_state, decision)
        return decision

    def start_game(self) -> None:
        pass
        
    run_turn = orchestrate

    def flush_all_logs(self) -> None:
        self._timer.flush_logs()
        self._analyst.flush_logs()
        from agents.strategy_agent_io import flush_logs as flush_strategy_logs
        from agents.orchestrator_log import flush_logs as flush_orch_logs
        flush_strategy_logs()
        flush_orch_logs()
