import json
import pathlib
from typing import Any

def _get_initial_actions(
    configuration: dict[str, Any],
) -> tuple[list[int], dict[str, Any]]:
    initial_actions = configuration.get("initialActions", [])
    if initial_actions:
        if configuration.get("useOpenings"):
            raise ValueError("Cannot set both useOpenings and initialActions.")
        else:
            return initial_actions, {}
    if not configuration.get("useOpenings"):
        return [], {}
    seed = configuration.get("seed", None)
    if seed is None:
        raise ValueError("Must provide seed if useOpenings is True.")
    openings_path = pathlib.Path(
        GAMES_DIR,
        configuration.get("openSpielGameName"),
        "openings.jsonl",
    )
    if not openings_path.is_file():
        raise ValueError(f"No opening file found at {openings_path}")
    with open(openings_path, "r", encoding="utf-8") as f:
        openings = f.readlines()
        opening = json.loads(openings[seed % len(openings)])
        initial_actions = opening.pop("initialActions")
        return initial_actions, opening

