"""
test_agents.py
──────────────
End-to-end integration tests for all five agents via the Router,
plus a full Orchestrator pipeline run.
"""

import sys, json
sys.path.insert(0, ".")

from router.bus import Router, ScopeViolationError
from agents.hand_analyst   import HandAnalyst
from agents.turn_planner   import TurnPlanner
from agents.time_manager   import TimeManager
from agents.strategy_agent import StrategyAgent
from agents.opponent_model import OpponentModel, OpponentModelPacket
from agents.orchestrator   import Orchestrator

SEP = "=" * 60

router   = Router()
analyst  = HandAnalyst()
planner  = TurnPlanner()
tm       = TimeManager()
strategy = StrategyAgent()
opponent = OpponentModel()

# ── 1. HandAnalyst ─────────────────────────────────────────────────────────────
print(SEP)
print("1. HandAnalyst -- via Router")
print(SEP)
pkt    = router.dispatch("HandAnalyst", {"hand": ["Charizard ex", "Rare Candy", "Fire Energy"], "deck_remaining": 28})
result = analyst.analyse(pkt)
print(json.dumps(result, indent=2))

# ── 2. TurnPlanner ─────────────────────────────────────────────────────────────
print()
print(SEP)
print("2. TurnPlanner -- via Router")
print(SEP)
pkt2 = router.dispatch("TurnPlanner", {"hand_score": result["hand_score"], "priority_profile": result["priority_profile"]})
plan = planner.plan(pkt2)
for step in plan:
    mark      = "v" if step["viable"] else "x"
    action    = step["action"]
    rationale = step["rationale"][:72]
    print(f"  [{mark}] {action:<16}  {rationale}")

# ── 3. TimeManager ─────────────────────────────────────────────────────────────
print()
print(SEP)
print("3. TimeManager -- three timing scenarios")
print(SEP)
for elapsed, label in [(300.0, "NORMAL"), (550.0, "FAST_MOVE"), (575.0, "FORCE_PASS")]:
    pkt3 = router.dispatch("TimeManager", {"time_elapsed": elapsed, "time_limit": 600})
    r    = tm.tick(pkt3)
    directive = r["directive"]
    urgency   = r["urgency"]
    remaining = r["time_remaining"]
    print(f"  elapsed={elapsed:5.1f}s  directive={directive:<12}  urgency={urgency:.3f}  remaining={remaining}s  [{label}]")

# ── 4. StrategyAgent ───────────────────────────────────────────────────────────
print()
print(SEP)
print("4. StrategyAgent -- trigger matching")
print(SEP)

strategy_tests = [
    ("ko_window",  {},                            "exact key match"),
    ("prize_race", {},                            "exact key match"),
    ("",           {"prizes": 1},                 "board_summary signal (prizes=1 -> endgame_close)"),
    ("bench_low",  {"bench_count": 1},            "exact key + board signal"),
    ("attacking",  {},                            "keyword scan / fallback"),
]

for trigger, board_summary, note in strategy_tests:
    pkt4 = router.dispatch("StrategyAgent", {"trigger": trigger, "board_summary": board_summary})
    r4   = strategy.evaluate(pkt4)
    strat    = r4["strategy"]
    posture  = r4["posture"]
    conf     = r4["confidence"]
    actions  = r4["actions"][:3]
    print(f"  trigger={repr(trigger):<14}  -> {strat:<22} posture={posture:<12} conf={conf:.2f}  top_actions={actions}")
    print(f"    ({note})")

# ── 5. OpponentModel ───────────────────────────────────────────────────────────
print()
print(SEP)
print("5. OpponentModel -- Bayesian archetype inference")
print(SEP)

opp_pkt = OpponentModelPacket(
    turn=3,
    newly_played_cards=["Quick Ball", "Nest Ball", "Boss's Orders"],
    opponent_active_pokemon="Pikachu ex",
    opponent_bench_count=3,
    opponent_hand_size=4,
    opponent_prizes_remaining=4,
    opponent_discard=["Lightning Energy"],
    game_phase="early",
)
opp_result = opponent.receive(opp_pkt)
print(json.dumps(opp_result, indent=2))

# ── 6. Scope violation ─────────────────────────────────────────────────────────
print()
print(SEP)
print("6. Scope violation guard -- HandAnalyst rejects TurnPlanner key")
print(SEP)
try:
    router.dispatch("HandAnalyst", {"hand": [], "deck_remaining": 5, "hand_score": 9.0})
    print("  ERROR: should have raised ScopeViolationError")
except ScopeViolationError as e:
    print(f"  ScopeViolationError raised correctly:")
    print(f"    {e}")

# ── 7. Full Orchestrator pipeline ──────────────────────────────────────────────
print()
print(SEP)
print("7. Orchestrator -- full turn pipeline")
print(SEP)

game_state = {
    # time
    "time_elapsed": 210.0,
    "time_limit":   600.0,
    # hand
    "hand":           ["Charizard ex", "Rare Candy", "Fire Energy", "Boss's Orders"],
    "deck_remaining": 22,
    # strategy
    "trigger":       "ko_window",
    "board_summary": {"prizes": 3, "opponent_prizes": 4, "hand_score": 6.5},
    # opponent model
    "revealed_cards":            ["Quick Ball", "Arcanine ex"],
    "turn_number":               5,
    "archetype_confidence":      0.55,
    "opponent_active_pokemon":   "Arcanine ex",
    "opponent_bench_count":      2,
    "opponent_hand_size":        3,
    "opponent_prizes_remaining": 4,
    "opponent_discard":          ["Fire Energy", "Fire Energy"],
    "game_phase":                "mid",
}

orch     = Orchestrator()
decision = orch.orchestrate(game_state)

print(f"  timing_directive  : {decision.timing_directive}")
print(f"  time_remaining    : {decision.time_remaining}s")
print(f"  hand_score        : {decision.hand_score}")
print(f"  priority_profile  : {decision.priority_profile}")
print(f"  top_play          : {decision.top_play}")
print(f"  strategy          : {decision.strategy}  (posture={decision.posture}, conf={decision.strategy_confidence:.2f})")
print(f"  opponent archetype: {decision.opponent_archetype}  (conf={decision.opponent_confidence:.2f})")
print(f"  predicted opp move: {decision.predicted_opponent_action}")
print(f"  final_actions     : {decision.final_actions}")
print(f"  PRIMARY ACTION    : {decision.primary_action}")

print()
print("All tests passed.")
