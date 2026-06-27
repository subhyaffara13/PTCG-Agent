"""agents/orchestrator.py -- Thin shell that owns Orchestrator.

Delegates step logic to orchestrator_steps.py and logging to orchestrator_log.py.
"""

from __future__ import annotations
from typing import Any

from router.bus import Router
from cb_agents.hand_analyst   import HandAnalyst
from cb_agents.turn_planner   import TurnPlanner
from cb_agents.time_manager   import TimeManager
from cb_agents.strategy_agent import StrategyAgent
from cb_agents.opponent_model import OpponentModel
from cb_agents.orchestrator_types import TurnDecision
from cb_agents.orchestrator_steps import (
    _step_time, _step_hand, _step_plan, _step_strategy, _step_opponent,
)
from cb_agents.orchestrator_merge import _merge, _emergency_pass
from cb_agents.orchestrator_log import _log_orchestration


class Orchestrator:
    def __init__(self) -> None:
        self._router   = Router()
        self._analyst  = HandAnalyst()
        self._planner  = TurnPlanner()
        self._timer    = TimeManager()
        self._strategy = StrategyAgent()
        self._opponent = OpponentModel()

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

    def flush_all_logs(self) -> None:
        self._timer.flush_logs()
        self._analyst.flush_logs()
        from cb_agents.strategy_agent_io import flush_logs as flush_strategy_logs
        from cb_agents.orchestrator_log import flush_logs as flush_orch_logs
        flush_strategy_logs()
        flush_orch_logs()
