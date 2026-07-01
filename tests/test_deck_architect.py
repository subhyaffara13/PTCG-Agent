"""
tests/test_deck_architect.py

Unit tests for factory/deck_architect.py.
"""
import json
import csv
import pytest
from factory.deck_architect import DeckArchitect
from test_deck_architect_helpers import (
    CARD_POOL_BASIC, CARD_POOL_REALISTIC, CSV_DATA, ARCHETYPES_DATA,
    make_skills_dir, make_decisions_file, make_staging_dir
)

def test_deck_architect_build_fallback(tmp_path):
    skills_dir = make_skills_dir(tmp_path)
    (skills_dir / "card_scoring.json").write_text(json.dumps(CARD_POOL_BASIC), encoding="utf-8")
    decisions_file = make_decisions_file(tmp_path)
    staging_dir = make_staging_dir(tmp_path)

    architect = DeckArchitect(
        log_dir=str(tmp_path), skills_dir=str(skills_dir),
        staging_dir=str(staging_dir), decisions_file=str(decisions_file)
    )
    res = architect.build({"next_eval_context": "aggro_test", "reasoning": "Tuning"})
    assert res["status"] == "success"

    csv_file = staging_dir / "deck_new.csv"
    assert csv_file.exists()
    total = sum(int(row["count"]) for row in csv.DictReader(open(csv_file, encoding="utf-8")))
    assert total == 60

def test_supercharged_deck_rules(tmp_path):
    skills_dir = make_skills_dir(tmp_path)
    (skills_dir / "card_scoring.json").write_text(json.dumps(CARD_POOL_REALISTIC), encoding="utf-8")
    (skills_dir / "card_pool_raw.csv").write_text(CSV_DATA, encoding="utf-8")
    (skills_dir / "deck_archetypes.json").write_text(json.dumps(ARCHETYPES_DATA), encoding="utf-8")
    decisions_file = make_decisions_file(tmp_path)
    staging_dir = make_staging_dir(tmp_path)

    architect = DeckArchitect(
        log_dir=str(tmp_path), skills_dir=str(skills_dir),
        staging_dir=str(staging_dir), decisions_file=str(decisions_file)
    )
    res = architect.build({"next_eval_context": "aggro", "reasoning": "Test architecture rules"})
    assert res["status"] == "success"

    deck_csv = staging_dir / "deck_new.csv"
    assert deck_csv.exists()
    deck_cards = {}
    for row in csv.DictReader(open(deck_csv, encoding="utf-8")):
        deck_cards[row["card_id"]] = int(row["count"])

    assert sum(deck_cards.values()) == 60
    assert deck_cards.get("basic-water-energy", 0) > 0
    assert deck_cards.get("basic-fire-energy", 0) == 0
    assert deck_cards.get("baxcalibur-par-060", 0) > 0
    assert deck_cards.get("frigibax-par-057", 0) > 0
    assert deck_cards.get("nest-ball-sv1-255", 0) > 0
    assert deck_cards.get("ultra-ball-sv1-196", 0) > 0
    assert deck_cards.get("professor-s-research-sv1-190", 0) > 0

def test_genetic_mutation_copy_limits():
    from scratch.deck_genetics import mutate_deck
    from collections import Counter
    card_a = {"card_id": 1, "card_type": "Pokemon", "card_name": "Pikachu"}
    card_b = {"card_id": 2, "card_type": "Trainer", "card_name": "Nest Ball"}
    card_energy = {"card_id": 3, "card_type": "Energy", "card_name": "Basic {W} Energy"}
    
    deck = [card_a]*4 + [card_b]*4 + [card_energy]*52
    pool_cards = [card_a, card_b, card_energy]
    details = {
        "1": {"card_id": 1, "card_name": "Pikachu", "card_type": "Pokemon"},
        "2": {"card_id": 2, "card_name": "Nest Ball", "card_type": "Trainer"},
        "3": {"card_id": 3, "card_name": "Basic {W} Energy", "card_type": "Energy"}
    }
    
    for _ in range(50):
        deck = mutate_deck(
            deck=deck,
            pokemon_pool=[card_a],
            basics=[card_a],
            energy_pool=[card_energy],
            trainer_pool={"Nest Ball": 4},
            pool_cards=pool_cards,
            details=details,
            mutation_rate=1.0
        )
        counts = Counter(c["card_id"] for c in deck)
        for cid, count in counts.items():
            card = next(x for x in pool_cards if x["card_id"] == cid)
            is_basic_energy = "ENERGY" in str(card.get("card_type")).upper() and "BASIC" in str(card.get("card_name", "")).upper()
            if not is_basic_energy:
                assert count <= 4, f"Card {card['card_name']} exceeded 4 copies: count is {count}"
