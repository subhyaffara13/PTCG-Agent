
def make_card_scoring(skills_dir):
    cards_file = skills_dir / "card_scoring.json"
    cards_file.write_text(json.dumps({
        "cards": [
            {"card_id": "1", "card_name": "Pikachu", "card_type": "Pokemon", "ev_score": 0.8, "combo_tags": ["Basic"]},
            {"card_id": "2", "card_name": "Supporter", "card_type": "Trainer", "ev_score": 0.6, "combo_tags": ["Supporter"]},
            {"card_id": "3", "card_name": "Energy", "card_type": "Energy", "ev_score": 0.5, "combo_tags": []}
        ]
    }), encoding="utf-8")
    return cards_file

