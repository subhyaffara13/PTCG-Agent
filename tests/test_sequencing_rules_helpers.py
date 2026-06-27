import json

def setup_skills_dir(tmp_path, filename, content):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    (skills_dir / filename).write_text(json.dumps(content), encoding="utf-8")
    return skills_dir

PRIORITY_RULES_EMPTY = {"rules": []}
STRATEGY_PROFILES_EMPTY = {"profiles": {}}

CHARGED_ACTIVE = {
    "id": 722,
    "energies": [3, 3, 3]
}
