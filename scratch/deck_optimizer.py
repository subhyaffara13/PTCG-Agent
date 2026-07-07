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
    top_candidates = run_generations(**data)

    if not top_candidates:
        print("No candidates generated. Exiting.")
        return

    # Stage 2: Verify the top candidates against the baseline deck in real simulations
    from concurrent.futures import ProcessPoolExecutor
    from factory.game_runner_worker import _parallel_game_worker
    from factory.game_runner import _load_optimized_deck, DEFAULT_DECK

    base_deck_ids = _load_optimized_deck("cb_agents/deck_base.csv")
    if not base_deck_ids:
        base_deck_ids = DEFAULT_DECK

    print(f"Stage 2: Evaluating top {len(top_candidates)} candidates using parallel game playouts...")
    
    best_deck = None
    best_win_rate = -1.0
    best_fitness = -float('inf')
    
    # Run 3 games for each of the 5 candidates (15 games total) in parallel
    executor = ProcessPoolExecutor(max_workers=16)
    futures = []
    for i, (fit, cand) in enumerate(top_candidates):
        cand_ids = [int(c["card_id"]) for c in cand]
        for g in range(3):
            label = f"opt_val_cand_{i}_game_{g}"
            f = executor.submit(
                _parallel_game_worker, 
                "logs", label, "base", f"cand_{i}", 
                base_deck_ids, cand_ids, False, False
            )
            futures.append((i, f))

    # Collect outcomes
    wins_map = {i: 0 for i in range(len(top_candidates))}
    total_map = {i: 0 for i in range(len(top_candidates))}
    
    for i, f in futures:
        try:
            res = f.result()
            total_map[i] += 1
            if res.get("winner") == "player_b":  # candidate is player_b
                wins_map[i] += 1
        except Exception as e:
            print(f"Error running game for candidate {i}: {e}")

    # Log and select best candidate
    for i, (fit, cand) in enumerate(top_candidates):
        wins = wins_map[i]
        total = total_map[i]
        win_rate = (wins / total) if total > 0 else 0.0
        print(f"  Candidate {i}: Stage 1 Fitness = {fit:.2f}, Simulated Win Rate = {win_rate:.2%} ({wins}/{total})")
        
        if win_rate > best_win_rate or (win_rate == best_win_rate and fit > best_fitness):
            best_win_rate = win_rate
            best_deck = cand
            best_fitness = fit

    executor.shutdown()

    final_copies = Counter(c["card_id"] for c in best_deck)
    seen = set()
    rows = [["card_id", "card_name", "card_type", "count"]]
    for c in best_deck:
        if c["card_id"] not in seen:
            rows.append([c["card_id"], c.get("card_name"), c.get("card_type"), final_copies[c["card_id"]]])
            seen.add(c["card_id"])
    csv.writer(Path("cb_agents/deck_new.csv").open("w", newline="", encoding="utf-8")).writerows(rows)
    print(f"Two-Stage Hybrid Search Completed. Best Selected Deck Win Rate: {best_win_rate:.2%}, Stage 1 Fitness: {best_fitness:.2f}")
    Path("logs/best_fitness.json").write_text(json.dumps({"best_fitness": best_fitness}), encoding="utf-8")

if __name__ == "__main__":
    main()
