import random

def _card_key(deck):
    return tuple(sorted(c["card_id"] for c in deck))

def _card_type_counts(deck, details):
    return (
        sum(1 for c in deck if c.get("card_type") == "Pokemon" and details.get(str(c["card_id"]), {}).get("stage") == "Basic"),
        sum(1 for c in deck if c.get("card_type") == "Energy"),
        sum(1 for c in deck if c.get("card_type") == "Trainer"),
    )

def mutate_deck(deck: list, pokemon_pool: list, basics: list, energy_pool: list,
                trainer_pool: dict, pool_cards: list, details: dict, mutation_rate: float = 0.3) -> list:
    result = list(deck)
    for idx in range(len(result)):
        if random.random() >= mutation_rate:
            continue
        c = result[idx]
        ctype = c.get("card_type")
        if ctype == "Pokemon":
            replacement = random.choice(pokemon_pool)
        elif ctype == "Energy":
            matching = [e for e in energy_pool if "{L}" in e.get("card_name", "")]
            replacement = random.choice(matching or energy_pool)
        elif ctype == "Trainer":
            trainer_names = list(trainer_pool.keys())
            tname = random.choice(trainer_names)
            replacement = next(
                (x for x in pool_cards if x.get("card_name", "").lower().replace("'", "'").replace("é", "e")
                 == tname.lower().replace("'", "'").replace("é", "e")), None)
            if replacement is None:
                continue
        else:
            continue
        if replacement is not None:
            result[idx] = replacement
    return result

def crossover_deck(a: list, b: list, pool_cards: list, details: dict) -> list:
    split = random.randint(15, 45)
    combined = a[:split] + b[split:]
    copies = {}
    result = []
    for c in combined:
        cid = str(c["card_id"])
        limit = 99 if c.get("card_type") == "Energy" and "Basic" in c.get("card_name", "") else 4
        if copies.get(cid, 0) < limit:
            result.append(c)
            copies[cid] = copies.get(cid, 0) + 1
    return result[:60]

def diversity_bonus(deck: list, population: list, details: dict) -> float:
    if len(population) < 5:
        return 0.0
    deck_ids = {str(c["card_id"]) for c in deck}
    avg_similarity = 0.0
    for other in population:
        other_ids = {str(c["card_id"]) for c in other}
        if not deck_ids or not other_ids:
            continue
        overlap = len(deck_ids & other_ids) / max(len(deck_ids | other_ids), 1)
        avg_similarity += overlap
    avg_similarity /= len(population)
    return (1.0 - avg_similarity) * 800.0
