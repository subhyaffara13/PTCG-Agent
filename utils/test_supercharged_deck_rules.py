
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

