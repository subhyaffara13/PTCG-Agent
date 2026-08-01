
def _load_preset_hands_from_file(configuration: dict[str, Any]) -> list[list[int]]:
    if configuration.get("openSpielGameName") != "repeated_poker":
        raise ValueError("loadPresetHands only supported for repeated_poker.")
    seed = configuration.get("seed", None)
    if seed is None:
        raise ValueError("Must provide seed if loadPresetHands is True.")
    preset_path = pathlib.Path(
        GAMES_DIR,
        configuration.get("openSpielGameName"),
        "preset_hands.jsonl",
    )
    if not preset_path.is_file():
        raise ValueError(f"No preset hands file found at {preset_path}")
    with open(preset_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        raise ValueError(f"Preset hands file at {preset_path} is empty.")
    entry = json.loads(lines[seed % len(lines)])
    preset_hands = entry.get("presetHands")
    if not preset_hands:
        raise ValueError("Preset hands entry missing presetHands data.")
    return preset_hands

