"""Integration smoke test for the full PTCG agent pipeline."""
import sys
sys.path.insert(0, ".")

# 1. StrategyAgent
from agents.strategy_agent import StrategyAgent
sa = StrategyAgent()
r = sa.evaluate({
    "trigger": "turn_start",
    "board_summary": {
        "own_prizes_remaining": 6,
        "opponent_prizes_remaining": 5,
        "energy_in_hand": 2,
        "turn_number": 1,
    }
})
print("[StrategyAgent] strategy:", r["strategy"], "| posture:", r["posture"])
assert r["strategy"] in sa._profiles, f"Unknown strategy: {r['strategy']}"

# 2. DeckArchitect
from factory.deck_architect import DeckArchitect
da = DeckArchitect()
rep = da.propose_mutation({"report_snapshot": {"deck_archetype": "aggro"}})
print("[DeckArchitect] targeted:", rep["dimension_targeted"],
      "| score:", rep["deck_score_before"], "->", rep["deck_score_after"])
assert 0 <= rep["deck_score_before"] <= 1
assert 0 <= rep["deck_score_after"]  <= 1

# 3. Orchestrator (single turn)
from agents.orchestrator import Orchestrator
orch = Orchestrator()
gs = {
    "hand": ["Professor's Research", "Basic Attacker", "Energy",
             "Energy", "Nest Ball", "Rare Candy", "Switch"],
    "deck_remaining": 52,
    "revealed_cards": [],
    "turn_number": 1,
    "archetype_confidence": 0.5,
    "time_elapsed": 0.0,
    "time_limit": 600.0,
    "board_summary": {
        "own_prizes_remaining": 6,
        "opponent_prizes_remaining": 6,
        "bench_pokemon_count": 0,
        "energy_in_hand": 2,
        "turn_number": 1,
        "opponent_bench_size": 2,
    },
}
turn_result = orch.run_turn(gs)
print("[Orchestrator]  action:", turn_result["action"], "| profile:", turn_result["profile"])
assert turn_result["action"] in ("ATTACK_KO", "EVOLVE", "ATTACH_ENERGY", "PLAY_TRAINER", "PASS")

# 4. GameRunner (full series)
from factory.game_runner import GameRunner
gr = GameRunner(agent_archetype="aggro", opponent_archetype="control", seed=42)
logs = gr.run_series()
assert len(logs) == 3, f"Expected 3 logs, got {len(logs)}"
for i, log in enumerate(logs, 1):
    wr = log["win_rate"]
    ko = log["ko_rate"]
    print(f"[GameRunner]    Game {i} win_rate={wr} ko_rate={ko}")

# 5. EvalAgent end-to-end
from factory.eval_agent import EvalAgent
ea = EvalAgent()
report = ea.evaluate(
    game_logs=logs,
    last_change_type="deck_swap",
    deck_archetype="aggro",
    version_tag="v0.2.0",
)
ctx = report["eval_context"]
adj = report["adjusted"]["version_score"]
print("[EvalAgent]     context:", ctx, "| adj version_score:", adj)
assert ctx == "aggro_test"

# 6. submission/main.py
from submission.main import agent
obs = {
    "hand": ["Professor's Research", "Basic Attacker", "Energy"],
    "deck_remaining": 50,
    "revealed_cards": [],
    "turn_number": 1,
    "archetype_confidence": 0.5,
    "own_prizes_remaining": 6,
    "opponent_prizes_remaining": 6,
    "bench_pokemon_count": 0,
    "energy_in_hand": 1,
    "time_elapsed": 0.0,
}
action = agent(obs, {"actTimeout": 600.0})
print("[submission]    agent() returned:", action)
assert isinstance(action, str)

print()
print("All integration checks passed.")
