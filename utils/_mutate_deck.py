
import random

def _mutate_deck(deck: list[int], mutation_rate: float = 0.30) -> list[int]:
    if len(deck) != 60:
        return deck
    if random.random() > mutation_rate:
        return deck
    d = list(deck)
    pool = list(set(deck))
    n_changes = random.randint(2, 5)
    for _ in range(n_changes):
        i = random.randrange(60)
        d[i] = random.choice(pool)
    return d

