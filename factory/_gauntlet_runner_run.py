import logging
logger = logging.getLogger("gauntlet_evaluator")

def _load_league_deck(league_file):
    if not league_file.exists():
        return None
    try:
        import csv
        deck = []
        with open(league_file, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                deck.extend([int(row["card_id"])] * int(row["count"]))
        return deck if len(deck) == 60 else None
    except Exception as e:
        logger.warning(f"Failed to load {league_file.name}: {e}")
        return None

def _generate_gauntlet_deck(generator, arch_lower, pool, details, archetypes_data):
    legal = [c for c in pool if c.get("archetype") == arch_lower or c.get("card_type") == "Energy"]
    basics = [c for c in pool if c.get("card_type") == "Pokemon" and details.get(str(c.get("card_id")), {}).get("stage") == "Basic"]
    energies = [c for c in pool if c.get("card_type") == "Energy"]
    try:
        cand = generator.generate_candidate(legal, basics, energies, arch_lower)
        return [int(c["card_id"]) for c in cand]
    except Exception as e:
        logger.warning(f"Failed to generate real deck: {e}")
        from factory.game_runner import DEFAULT_DECK
        return list(DEFAULT_DECK)

def execute_gauntlet_games(runner, archetype, opp_deck, target_deck, num_games):
    total_wins = total_games = 0
    for i in range(num_games):
        res = runner.run_iteration(iteration_id=9999, version_n1="candidate", version_n2=f"gauntlet_{archetype}", deck_base=target_deck, deck_new=opp_deck, reasoning_base={}, reasoning_new={}, num_matchups=1)
        games = res.get("games", {})
        total_games += len(games)
        for game in games.values():
            if game.get("winner") == "player_a":
                total_wins += 1
    return total_wins, total_games
