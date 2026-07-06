"""Integration smoke test for the full PTCG agent pipeline."""
import sys
sys.path.insert(0, ".")

# 1. StrategyAgent (uses receive() with StrategyPacket)
print("=" * 60)
print("1. StrategyAgent")
from agents.strategy_agent import StrategyAgent
from router.bus import StrategyPacket

sa = StrategyAgent()
packet = StrategyPacket(
    trigger="turn_start",
    board_summary={
        "my_prizes_remaining": 6,
        "opponent_prizes_remaining": 5,
        "energy_in_hand": 2,
        "turn_number": 1,
    }
)
r = sa.receive(packet)
print(f"  strategy: {r['strategy']} | posture: {r['posture']} | confidence: {r['confidence']}")
assert "strategy" in r, f"Missing 'strategy' key in response"
print("  PASSED")

# 2. DeckArchitect
print("=" * 60)
print("2. DeckArchitect")
from factory.deck_architect import DeckArchitect
da = DeckArchitect()
rep = da.build({"next_eval_context": "aggro", "reasoning": "low deck delta"})
print(f"  status: {rep['status']} | score: {rep.get('deck_score', 'N/A')}")
assert rep["status"] == "success", f"DeckArchitect failed: {rep}"
assert 0 <= rep["deck_score"] <= 1
print("  PASSED")

# 3. Orchestrator (single turn)
print("=" * 60)
print("3. Orchestrator (full turn pipeline)")
from agents.orchestrator import Orchestrator
orch = Orchestrator()
orch.start_game()

gs = {
    "my_hand": ["Professor's Research", "Basic Attacker", "Energy",
             "Energy", "Nest Ball", "Rare Candy", "Switch"],
    "my_deck_count": 52,
    "my_discard": [],
    "my_board": [],
    "my_bench": [],
    "my_prizes": 6,
    "my_active_hp": 100,
    "my_active_damage": 30,
    "opponent_prizes": 6,
    "opponent_active_hp": 100,
    "opponent_active": None,
    "opponent_bench": [],
    "opponent_hand_count": 5,
    "opponent_discard": [],
    "opponent_last_play": None,
    "opponent_revealed": None,
    "turn_number": 1,
    "legal_attacks": ["Thunder Shock"],
    "legal_evolutions": [],
    "legal_attachments": ["energy_1"],
    "legal_trainers": ["Professor's Research", "Nest Ball"],
    "legal_bench": ["Basic Attacker"],
    "legal_retreats": [],
}
decision = orch.run_turn(gs)
action = decision.primary_action if hasattr(decision, "primary_action") else decision
print(f"  action returned: {action}")
assert isinstance(action, str), f"Expected str, got {type(action)}"
print("  PASSED")

# 4. Multi-turn simulation
print("=" * 60)
print("4. Orchestrator (3-turn simulation)")
for turn in range(2, 5):
    gs["turn_number"] = turn
    gs["my_deck_count"] = max(0, 52 - turn * 2)
    gs["my_prizes"] = max(1, 6 - (turn - 1))
    decision = orch.run_turn(gs)
    action = decision.primary_action if hasattr(decision, "primary_action") else decision
    print(f"  Turn {turn}: {action}")
    assert isinstance(action, str)
print("  PASSED")

# 5. Flush all logs
print("=" * 60)
print("5. Log flushing")
orch.flush_all_logs()
print("  All agent logs flushed successfully")
print("  PASSED")

print()
print("=" * 60)
print("All integration checks passed!")
