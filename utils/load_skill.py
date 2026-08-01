
def load_skill(skills_dir=None) -> dict[str, dict[str, Any]]:
    path = pathlib.Path(skills_dir) / "strategy_profiles.json" if skills_dir else _SKILL_PATH
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raw = {"profiles": {}}
    return raw.get("profiles", {})


def load_skill(skills_dir=None) -> dict[str, dict[str, Any]]:
    path = pathlib.Path(skills_dir) / "strategy_profiles.json" if skills_dir else _SKILL_PATH
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raw = {"profiles": {}}
    return raw.get("profiles", {})


def load_skill(skills_dir=None) -> dict[str, dict[str, Any]]:
    path = pathlib.Path(skills_dir) / "strategy_profiles.json" if skills_dir else _SKILL_PATH
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raw = {"profiles": {}}
    return raw.get("profiles", {})

