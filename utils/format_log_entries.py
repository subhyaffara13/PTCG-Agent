import json
from pathlib import Path


def format_log_entries(component: str, path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data:
        return "Logs are empty."
    latest = data[-3:]
    msg = f"**📊 Latest Heuristic Reasoning for `{component}`:**\n"
    for i, entry in enumerate(latest):
        msg += f"\n**Turn {entry.get('turn')} ({entry.get('perspective')}):**\n```json\n"
        cleaned_entry = {k: v for k, v in entry.items() if k not in ("turn", "perspective")}
        msg += json.dumps(cleaned_entry, indent=2)[:500]
        msg += "\n```"
    return msg

