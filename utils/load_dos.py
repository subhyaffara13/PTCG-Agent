
def load_dos(dos_file: Path) -> Dict[str, Any]:
    if dos_file.exists():
        try:
            return json.loads(dos_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {
        "deck_dos": [],
        "behavior_dos": [],
        "setup_profiles": [],
        "deck_stats": {}
    }

