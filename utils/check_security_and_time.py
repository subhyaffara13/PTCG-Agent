import re
from pathlib import Path


def check_security_and_time(staged_path: Path, content: str) -> tuple[int, str]:
    lines = content.splitlines()

    # Router Bus Boundaries (Check 4)
    state_pattern = re.compile(r'\b(GameState|OrchestratorState)\b')
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if state_pattern.search(line):
            return 4, f"Access to full state object found on line {idx}"
        if "RouterBus." in line and not (".dispatch(" in line):
            return 4, f"Direct access to RouterBus internals on line {idx}"

    # Auto-Submit (Check 5)
    forbidden_words = ["kaggle", "submit", "api_key", "upload", "competition"]
    for idx, line in enumerate(lines, start=1):
        for word in forbidden_words:
            if word in line.lower() and f"#{word}" not in line.lower() and "import" not in line.lower():
                return 5, f"Auto-submit string '{word}' found on line {idx}"

    # API Keys (Check 6)
    key_pattern = re.compile(r'["\'](sk-[A-Za-z0-9]{15,}|AIza[A-Za-z0-9_-]{15,}|Bearer\s+[A-Za-z0-9_-]{15,})["\']')
    long_string_pattern = re.compile(r'["\']([A-Za-z0-9]{20,})["\']')
    for idx, line in enumerate(lines, start=1):
        if key_pattern.search(line):
            return 6, f"Hardcoded key pattern found on line {idx}: [REDACTED]"
        for match in long_string_pattern.finditer(line):
            val = match.group(1)
            if any(c.islower() for c in val) and any(c.isupper() for c in val) and any(c.isdigit() for c in val):
                return 6, f"Suspected high-entropy key on line {idx}: [REDACTED]"

    # Time compliance (Check 7)
    if staged_path.name == "game_runner.py":
        if not any("600" in line for line in lines):
            return 7, "Forced game timeout (600s) check missing in game_runner.py"
        if not any("540" in line for line in lines):
            return 7, "Fastest legal move check at 540s missing in game_runner.py"
        if not any("570" in line for line in lines):
            return 7, "Forced pass check at 570s missing in game_runner.py"

    return 0, ""

