"""Helper functions extracted from deck_ga_engine.py."""

from scratch.deck_simulator import evaluate_single_candidate
from scratch.deck_surrogate import build_training_data, train_surrogate_model, optimize_via_surrogate


def surrogate_dreaming(pool_cards, details, scores, pokemon_pool,
                       basics, energy_pool, trainer_pool, seed_deck):
    print("[Surrogate] Generating training data...")
    training_data = build_training_data(pool_cards, details, scores, pokemon_pool,
                                        basics, energy_pool, trainer_pool, n_samples=300)
    if training_data:
        print(f"[Surrogate] Training on {len(training_data)} decks...")
        model, cards, card_index, max_cp, embeddings_t = train_surrogate_model(
            pool_cards, details, scores, training_data, epochs=120)
        dream_seeds = []
        for i in range(2):
            print(f"[Surrogate] Dreaming deck {i+1}...")
            dream = optimize_via_surrogate(model, cards, card_index, max_cp, embeddings_t,
                                           pool_cards, details, scores, steps=300)
            if len(dream) == 60 and not all(c.get("card_type") == "Energy" for c in dream):
                fit = evaluate_single_candidate((dream, scores, details))
                dream_seeds.append((dream, fit))
                print(f"[Surrogate] Dream deck {i+1} fitness: {fit:.2f}")
        if dream_seeds:
            best_dream = max(dream_seeds, key=lambda x: x[1])
            print(f"[Surrogate] Best dream seed fitness: {best_dream[1]:.2f}, comparing against seed_deck...")
            seed_fit = evaluate_single_candidate((seed_deck, scores, details)) if len(seed_deck) == 60 else -float('inf')
            if best_dream[1] > seed_fit:
                seed_deck = best_dream[0]
    return seed_deck
