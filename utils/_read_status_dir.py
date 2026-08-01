
def _read_status_dir(status_dir: str) -> list[dict[str, Any]]:
    """Snapshot of all in-flight cells. Tolerates partial writes / races."""
    out: list[dict[str, Any]] = []
    try:
        names = os.listdir(status_dir)
    except FileNotFoundError:
        return out
    for name in names:
        if not name.endswith(".json"):
            continue
        try:
            with open(os.path.join(status_dir, name)) as f:
                out.append(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            continue
    return out

