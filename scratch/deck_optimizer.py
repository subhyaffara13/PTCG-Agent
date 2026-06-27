"""
scratch/deck_optimizer.py
Genetic Algorithm deck optimizer using parallel evaluations and memoization.
"""
import sys
import csv
import json
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

from scratch.deck_setup import load_optimizer_data
from scratch.deck_ga_engine import run_generations

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--archetype", type=str, default=None,
                        help="Archetype to focus on (aggro, combo, control, utility). "
                             "Defaults to dominant archetype from winning decks.")
    args = parser.parse_args()
    data = load_optimizer_data(archetype=args.archetype)
    best_deck, best_fitness = run_generations(**data)

    final_copies = Counter(c["card_id"] for c in best_deck)
    seen = set()
    rows = [["card_id", "card_name", "card_type", "count"]]
    for c in best_deck:
        if c["card_id"] not in seen:
            rows.append([c["card_id"], c.get("card_name"), c.get("card_type"), final_copies[c["card_id"]]])
            seen.add(c["card_id"])
    csv.writer(Path("agents/deck_new.csv").open("w", newline="", encoding="utf-8")).writerows(rows)
    print(f"Parallel GA Search Completed. Best fitness: {best_fitness:.2f}")
    Path("logs/best_fitness.json").write_text(json.dumps({"best_fitness": best_fitness}), encoding="utf-8")

if __name__ == "__main__":
    main()
