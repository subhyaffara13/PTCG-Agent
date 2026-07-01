import random
import math

from scratch.deck_builder import make_deck
from scratch.deck_simulator import evaluate_single_candidate
from scratch.deck_genetics import _card_key, mutate_deck
from scratch.deck_milp import optimize_deck_milp
from scratch.configs import GEN_LIMIT, SA_INITIAL_TEMP, SA_COOLING_RATE, SA_REHEAT_THRESHOLD, SA_GEN_LIMIT
from scratch.deck_ga_engine_parts import surrogate_dreaming
from scratch.deck_beam_builder import BeamDeckBuilder, extract_packages


def run_generations(pool_cards, details, scores, pokemon_pool, basics,
                    energy_pool, trainer_pool, seed_deck, empirical_core=None):
    best_deck, best_fitness = None, -float('inf')
    empirical_core = empirical_core or []

    seeds = []

    sd = surrogate_dreaming(pool_cards, details, scores, pokemon_pool,
                                   basics, energy_pool, trainer_pool, seed_deck)
    if sd and len(sd) == 60:
        seeds.append(sd)

    if empirical_core:
        milp_sd = optimize_deck_milp(empirical_core, pool_cards, details, scores)
        if milp_sd and len(milp_sd) == 60:
            seeds.append(milp_sd)

    id_map = {int(c["card_id"]): c for c in pool_cards}
    pkgs = extract_packages(id_map)
    if pkgs:
        beam_builder = BeamDeckBuilder(pkgs)
        beam_deck = beam_builder.build(id_map)
        if beam_deck:
            beam_deck_full = optimize_deck_milp(beam_deck, pool_cards, details, scores)
            if beam_deck_full and len(beam_deck_full) == 60:
                seeds.append(beam_deck_full)

    if not seeds:
        p_lines = random.sample(pokemon_pool[:max(1, len(pokemon_pool)//2)],
                                min(len(pokemon_pool), random.randint(1, 3)))
        seeds.append(make_deck(p_lines, trainer_pool, energy_pool, basics, pool_cards, details))

    best_seed = seeds[0]
    best_seed_fitness = evaluate_single_candidate((best_seed, scores, details))
    
    for s in seeds[1:]:
        f = evaluate_single_candidate((s, scores, details))
        if f > best_seed_fitness:
            best_seed_fitness = f
            best_seed = s
            
    current_deck = best_seed
    current_fitness = best_seed_fitness
    best_deck, best_fitness = current_deck, current_fitness

    fitness_cache = {_card_key(current_deck): current_fitness}

    # Track top candidates for Stage 2 verification
    top_candidates = [(current_fitness, current_deck)]

    initial_temp = SA_INITIAL_TEMP
    cooling_rate = SA_COOLING_RATE
    gen_limit = SA_GEN_LIMIT

    temp = initial_temp
    no_improve_count = 0
    for step in range(gen_limit):
        mutant = mutate_deck(current_deck, pokemon_pool, basics, energy_pool,
                             trainer_pool, pool_cards, details, 0.1, empirical_core=empirical_core)

        if len(mutant) != 60:
            continue

        k = _card_key(mutant)
        if k in fitness_cache:
            mutant_fitness = fitness_cache[k]
        else:
            mutant_fitness = evaluate_single_candidate((mutant, scores, details))
            fitness_cache[k] = mutant_fitness

        # Keep track of unique top 5 candidates
        if mutant_fitness > best_fitness:
            best_fitness = mutant_fitness
            best_deck = mutant
            no_improve_count = 0
        else:
            no_improve_count += 1

        # Add to top candidates if unique
        if not any(_card_key(mutant) == _card_key(tc[1]) for tc in top_candidates):
            top_candidates.append((mutant_fitness, mutant))
            top_candidates.sort(key=lambda x: x[0], reverse=True)
            top_candidates = top_candidates[:5]

        delta = mutant_fitness - current_fitness
        if delta > 0 or random.random() < math.exp(delta / max(temp, 1e-5)):
            current_deck = mutant
            current_fitness = mutant_fitness

        temp *= cooling_rate
        if no_improve_count >= SA_REHEAT_THRESHOLD:
            temp *= 2
            no_improve_count = 0

    final_polished = optimize_deck_milp(best_deck, pool_cards, details, scores)
    if len(final_polished) == 60:
        final_fitness = evaluate_single_candidate((final_polished, scores, details))
        if final_fitness > best_fitness:
            best_deck = final_polished
            best_fitness = final_fitness
            if not any(_card_key(best_deck) == _card_key(tc[1]) for tc in top_candidates):
                top_candidates.append((best_fitness, best_deck))
                top_candidates.sort(key=lambda x: x[0], reverse=True)
                top_candidates = top_candidates[:5]

    return top_candidates
