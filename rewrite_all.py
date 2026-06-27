"""
rewrite_all.py
--------------
Rewrites router/bus.py, agents/hand_analyst.py, agents/turn_planner.py,
agents/time_manager.py, agents/strategy_agent.py, agents/orchestrator.py
with the correct implementations, overwriting any stale content.
"""

import pathlib

from rewrite_all_cfg_bus import BUS
from rewrite_all_cfg_bus_b import BUS_B
from rewrite_all_cfg_hand import HAND_ANALYST
from rewrite_all_cfg_hand_b import HAND_ANALYST_B
from rewrite_all_cfg_planner import TURN_PLANNER
from rewrite_all_cfg_planner_b import TURN_PLANNER_B
from rewrite_all_cfg_time import TIME_MANAGER
from rewrite_all_cfg_strat_a import STRATEGY_AGENT_A
from rewrite_all_cfg_strat_b import STRATEGY_AGENT_B
from rewrite_all_cfg_orch_a import ORCHESTRATOR_A
from rewrite_all_cfg_orch_a2 import ORCHESTRATOR_A2
from rewrite_all_cfg_orch_b import ORCHESTRATOR_B

ROOT = pathlib.Path(__file__).parent

files = {
    ROOT / "router" / "bus.py":             BUS + BUS_B,
    ROOT / "agents" / "hand_analyst.py":    HAND_ANALYST + HAND_ANALYST_B,
    ROOT / "agents" / "turn_planner.py":    TURN_PLANNER + TURN_PLANNER_B,
    ROOT / "agents" / "time_manager.py":    TIME_MANAGER,
    ROOT / "agents" / "strategy_agent.py":  STRATEGY_AGENT_A + STRATEGY_AGENT_B,
    ROOT / "agents" / "orchestrator.py":    ORCHESTRATOR_A + ORCHESTRATOR_A2 + ORCHESTRATOR_B,
}

for path, content in files.items():
    path.write_text(content, encoding="utf-8")
    print(f"Written  {path.relative_to(ROOT)}  ({path.stat().st_size} bytes)")

print("\nAll files written successfully.")
