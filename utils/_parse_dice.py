
def _parse_dice(observation: str) -> list[dict[str, Any]]:
    for line in observation.splitlines():
        if line.startswith("Dice:"):
            payload = line[len("Dice:") :].strip()
            return [{"value": int(value), "used": used == "u"} for value, used in _DIE_RE.findall(payload)]
    return []

