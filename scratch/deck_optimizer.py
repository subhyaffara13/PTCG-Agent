"""
scratch/deck_optimizer.py
Genetic Algorithm deck optimizer using parallel evaluations and memoization.
"""
import sys
import csv
import json
import random
from pathlib import Path
from collections import Counter
from multiprocessing import Pool
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

from factory.deck_loader import DeckLoader
from scratch.deck_optimizer_helpers import (
    evaluate_single_candidate, make_deck,
    multivariate_setup_prob, evaluate_deck_synergy
)

def main():
    loader = DeckLoader(Path("skills"))
    pool_cards = loader.load_card_pool()
    details = loader.parse_card_details(pool_cards)
    data = json.loads(Path("logs/kaggle_summary/scraped_decks.json").read_text(encoding="utf-8"))
    w_opp, w_us, l_us = data.get("opp_wins", {}), data.get("us_wins", {}), data.get("us_losses", {})
    winning_decks = data.get("opp_win_decks", []) + data.get("us_win_decks", [])
    
    # Dynamic Meta-Counter Scorer
    opp_types = [details.get(str(cid), {}).get("element_type", "") for dk in data.get("opp_win_decks", []) for cid in dk]
    dominant_type = Counter(x for x in opp_types if x).most_common(1)
    bonus_type = {"{L}": "{F}", "{R}": "{W}", "{W}": "{L}", "{D}": "{F}", "{P}": "{D}", "{G}": "{R}"}.get(dominant_type[0][0]) if dominant_type else None
    
    winning_freq = Counter(int(cid) for dk in winning_decks for cid in dk)
    scores = {str(c["card_id"]): float(c.get("ev_score", 0.5)) + 2.0 * w_opp.get(str(c["card_id"]), 0) + 1.0 * w_us.get(str(c["card_id"]), 0) - 1.5 * l_us.get(str(c["card_id"]), 0) + 3.0 * winning_freq.get(int(c["card_id"]), 0) + (15.0 if bonus_type and details.get(str(c["card_id"]), {}).get("element_type") == bonus_type else 0.0) for c in pool_cards}
              
    winning_ids = set().union(*winning_decks)
    allowed_types = {details.get(str(cid), {}).get("element_type") for cid in winning_ids if details.get(str(cid), {}).get("element_type")}
    
    pokemon_pool = sorted([c for c in pool_cards if c.get("card_type") == "Pokemon" and details.get(str(c.get("card_id")), {}).get("element_type") in allowed_types], key=lambda x: scores.get(str(x["card_id"]), 0.0), reverse=True)
    basics = [c for c in pokemon_pool if details.get(str(c["card_id"]), {}).get("stage") == "Basic"]
    trainer_pool = {"ultra ball": 4, "nest ball": 4, "professor's research": 4, "iono": 4, "switch": 2, "boss's orders": 2}
    energy_pool = [c for c in pool_cards if c.get("card_type") == "Energy"]

    id_map = {int(c["card_id"]): c for c in pool_cards if str(c.get("card_id", "")).isdigit()}
    seed_deck = []
    p = Path("agents/deck_new.csv")
    if p.exists():
        for r in list(csv.reader(p.open(encoding="utf-8")))[1:]:
            if r: seed_deck.extend([id_map[int(r[0])]] * int(r[3]))
                
    best_deck, best_fitness = None, -float('inf')
    fitness_cache = {}
    
    with Pool() as p_pool:
        for gen in range(gen_limit := 100):
            candidates = [seed_deck] if gen == 0 and len(seed_deck) == 60 else []
            tries = 0
            while len(candidates) < 50 and tries < 500:
                tries += 1
                p_lines = random.sample(pokemon_pool[:max(1, len(pokemon_pool)//2)], min(len(pokemon_pool), random.randint(1, 3)))
                e_lines = random.sample(energy_pool, min(len(energy_pool), 2))
                cand = make_deck(p_lines, trainer_pool, e_lines, basics, pool_cards, details)
                n_basics = sum(1 for c in cand if c.get("card_type") == "Pokemon" and details.get(str(c["card_id"]), {}).get("stage") == "Basic")
                n_energies = sum(1 for c in cand if c.get("card_type") == "Energy")
                n_trainers = sum(1 for c in cand if c.get("card_type") == "Trainer")
                if tries > 400 or (multivariate_setup_prob(n_basics, n_energies, n_trainers) >= 0.85 and evaluate_deck_synergy(cand, details) <= 10.0):
                    candidates.append(cand)
                
            uncached, cached_indices = [], {}
            for i, cand in enumerate(candidates):
                k = tuple(sorted(c["card_id"] for c in cand))
                if k in fitness_cache: cached_indices[i] = fitness_cache[k]
                else: uncached.append((i, cand))
            if uncached:
                results = p_pool.map(evaluate_single_candidate, [(cand, scores, details) for _, cand in uncached])
                for (i, cand), fit in zip(uncached, results):
                    k = tuple(sorted(c["card_id"] for c in cand))
                    fitness_cache[k] = cached_indices[i] = fit
                    
            for i, fit in cached_indices.items():
                if fit > best_fitness:
                    best_fitness = fit
                    best_deck = candidates[i]

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
