import random
import math

from scratch.deck_builder import make_deck
from scratch.deck_simulator import evaluate_single_candidate
from scratch.deck_genetics import _card_key, mutate_deck
from scratch.deck_milp import optimize_deck_milp
from scratch.configs import GEN_LIMIT
from scratch.deck_ga_engine_parts import surrogate_dreaming


def run_generations(pool_cards, details, scores, pokemon_pool, basics,
                    energy_pool, trainer_pool, seed_deck, empirical_core=None):
    best_deck, best_fitness = None, -float('inf')
    empirical_core = empirical_core or []

    seed_deck = surrogate_dreaming(pool_cards, details, scores, pokemon_pool,
                                   basics, energy_pool, trainer_pool, seed_deck)

    current_deck = optimize_deck_milp(empirical_core, pool_cards, details, scores) if empirical_core else seed_deck

    if len(current_deck) != 60:
        p_lines = random.sample(pokemon_pool[:max(1, len(pokemon_pool)//2)],
                                min(len(pokemon_pool), random.randint(1, 3)))
        current_deck = make_deck(p_lines, trainer_pool, energy_pool, basics, pool_cards, details)

    current_fitness = evaluate_single_candidate((current_deck, scores, details))
    best_deck, best_fitness = current_deck, current_fitness

    fitness_cache = {_card_key(current_deck): current_fitness}

    initial_temp = 10.0
    cooling_rate = 0.95

    temp = initial_temp
    for step in range(GEN_LIMIT):
        mutant = mutate_deck(current_deck, pokemon_pool, basics, energy_pool,
                             trainer_pool, pool_cards, details, 0.1)

        if empirical_core:
            core_ids = [str(c["card_id"]) for c in empirical_core]
            mutant_ids = [str(c["card_id"]) for c in mutant]
            valid = True
            for cid in set(core_ids):
                if mutant_ids.count(cid) < core_ids.count(cid):
                    valid = False
                    break
            if not valid:
                mutant = optimize_deck_milp(empirical_core, pool_cards, details, scores)

        if len(mutant) != 60:
            continue

        k = _card_key(mutant)
        if k in fitness_cache:
            mutant_fitness = fitness_cache[k]
        else:
            mutant_fitness = evaluate_single_candidate((mutant, scores, details))
            fitness_cache[k] = mutant_fitness

        if mutant_fitness > best_fitness:
            best_fitness = mutant_fitness
            best_deck = mutant

        delta = mutant_fitness - current_fitness
        if delta > 0 or random.random() < math.exp(delta / max(temp, 1e-5)):
            current_deck = mutant
            current_fitness = mutant_fitness

        temp *= cooling_rate

    final_polished = optimize_deck_milp(best_deck, pool_cards, details, scores)
    if len(final_polished) == 60:
        final_fitness = evaluate_single_candidate((final_polished, scores, details))
        if final_fitness > best_fitness:
            best_deck = final_polished
            best_fitness = final_fitness

    return best_deck, best_fitness
