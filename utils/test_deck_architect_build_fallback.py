import json

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

