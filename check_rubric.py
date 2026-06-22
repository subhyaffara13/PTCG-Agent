import json
from pathlib import Path

# Reset eval state
state = {"consecutive_deck_failures": 0, "consecutive_logic_failures": 0}
Path("logs/eval_state.json").write_text(json.dumps(state, indent=2))
print("Eval state reset.")

# Verify rubric sums to 1.0 per context
rubric = json.loads(Path("skills/eval_rubric.json").read_text())
for ctx, weights in rubric["contexts"].items():
    total = sum(weights.values())
    wr = weights["win_rate"]
    print(f"  {ctx}: sum={total:.2f}  win_rate={wr}")
