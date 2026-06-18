"""
tests/test_deck_architect.py

Unit tests for factory/deck_architect.py.
"""

import os
import csv
import json
import pytest
from pathlib import Path
from factory.deck_architect import DeckArchitect

def test_deck_architect_build_fallback(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    
    # Save a minimal card pool
    cards_file = skills_dir / "card_scoring.json"
    cards_file.write_text(json.dumps({
        "cards": [
            {"card_id": "SV-1", "card_name": "Pikachu", "card_type": "Pokemon", "archetype": "aggro", "combo_tags": ["Basic"]},
            {"card_id": "SV-2", "card_name": "Lightning Energy", "card_type": "Energy", "archetype": "utility", "combo_tags": []}
        ]
    }), encoding="utf-8")

    decisions_file = tmp_path / "decisions.md"
    decisions_file.write_text("# Decisions\n", encoding="utf-8")

    staging_dir = tmp_path / "staging"
    staging_dir.mkdir()

    architect = DeckArchitect(
        log_dir=str(tmp_path),
        skills_dir=str(skills_dir),
        staging_dir=str(staging_dir),
        decisions_file=str(decisions_file)
    )

    notes = {"next_eval_context": "aggro_test", "reasoning": "Tuning"}
    res = architect.build(notes)
    
    assert res["status"] == "success"
    
    # Verify exact file count created
    csv_file = staging_dir / "deck_new.csv"
    assert csv_file.exists()
    
    # Read and ensure sum of card count is exactly 60
    total_cards = 0
    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_cards += int(row["count"])
            
    assert total_cards == 60
