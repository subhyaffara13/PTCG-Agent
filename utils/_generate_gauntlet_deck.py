
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

