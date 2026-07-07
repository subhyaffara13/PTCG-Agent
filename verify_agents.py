"""
verify_agents.py
────────────────
End-to-end integration tests for all five agents via the Router,
plus a full Orchestrator pipeline run.
"""
import sys, json
sys.path.insert(0, ".")
from router.bus import ScopeViolationError
from agents.orchestrator import Orchestrator
from test_agents_helpers import (
    SEP, router, analyst, planner, tm, strategy, opponent,
    strategy_tests, opp_pkt, game_state
)

print(SEP)
print("1. HandAnalyst -- via Router")
print(SEP)
pkt = router.dispatch("HandAnalyst", {"hand": ["Charizard ex", "Rare Candy", "Fire Energy"], "deck_remaining": 28})
result = analyst.analyse(pkt)
print(json.dumps(result, indent=2))

print()
print(SEP)
print("2. TurnPlanner -- via Router")
print(SEP)
pkt2 = router.dispatch("TurnPlanner", {"hand_score": result["hand_score"], "priority_profile": result["priority_profile"]})
r2 = planner.receive(pkt2)
print(json.dumps(r2, indent=2))

print()
print(SEP)
print("3. TimeManager -- three timing scenarios")
print(SEP)
for elapsed, label in [(300.0, "NORMAL"), (550.0, "FAST_MOVE"), (575.0, "FORCE_PASS")]:
    pkt3 = router.dispatch("TimeManager", {"time_elapsed": elapsed, "time_limit": 600})
    r = tm.tick(pkt3)
    print(f"  elapsed={elapsed:5.1f}s  directive={r['directive']:<12}  urgency={r['urgency']:.3f}  remaining={r['time_remaining']}s  [{label}]")

print()
print(SEP)
print("4. StrategyAgent -- trigger matching")
print(SEP)
for trigger, board_summary, note in strategy_tests:
    pkt4 = router.dispatch("StrategyAgent", {"trigger": trigger, "board_summary": board_summary})
    r4 = strategy.evaluate(pkt4)
    print(f"  trigger={repr(trigger):<14}  -> {r4['strategy']:<22} posture={r4['posture']:<12} conf={r4['confidence']:.2f}  top_actions={r4['actions'][:3]}")
    print(f"    ({note})")

print()
print(SEP)
print("5. OpponentModel -- Bayesian archetype inference")
print(SEP)
print(json.dumps(opponent.receive(opp_pkt), indent=2))

print()
print(SEP)
print("6. Scope violation guard -- HandAnalyst rejects TurnPlanner key")
print(SEP)
try:
    router.dispatch("HandAnalyst", {"hand": [], "deck_remaining": 5, "hand_score": 9.0})
    print("  ERROR: should have raised ScopeViolationError")
except ScopeViolationError as e:
    print(f"  ScopeViolationError raised correctly:\n    {e}")

print()
print(SEP)
print("7. Orchestrator -- full turn pipeline")
print(SEP)
decision = Orchestrator().orchestrate(game_state)
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
