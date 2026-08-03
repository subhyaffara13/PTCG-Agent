import json
import pathlib
from typing import Any

def _get_image_config(configuration: dict[str, Any]) -> dict[str, Any]:
    use_image = configuration.get("useImage", None)
    if use_image is None:
        raise ValueError("_get_image_config called but useImage missing from env config.")
    if not use_image:
        raise ValueError("_get_image_config called but useImage is False.")
    seed = configuration.get("seed", None)
    if seed is None:
        raise ValueError("Must provide seed if useImage is True.")
    image_config_path = pathlib.Path(
        GAMES_DIR,
        configuration.get("openSpielGameName"),
        "image_config.jsonl",
    )
    if not image_config_path.is_file():
        raise ValueError(f"No image config file found at {image_config_path}")
    with open(image_config_path, "r", encoding="utf-8") as f:
        image_configs = f.readlines()
        image_config = json.loads(image_configs[seed % len(image_configs)])
        return image_config

