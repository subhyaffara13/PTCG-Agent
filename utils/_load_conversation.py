import json
from typing import Any, Dict, List, Optional

def _load_conversation(
    console: Console, command: str, system: Optional[str]
) -> List[Dict[str, Any]]:
    """Load conversation from a file"""
    parts = command.split()
    if len(parts) < 2:
        console.print("[red]Usage: /load <filename>[/red]")
        return []

    filename = parts[1]
    if not filename.endswith(".json"):
        filename += ".json"

    try:
        with open(filename, "r") as f:
            messages = json.load(f)
        console.print(f"[green]Conversation loaded from {filename}[/green]")
        return messages
    except FileNotFoundError:
        console.print(f"[red]File not found: {filename}[/red]")
    except Exception as e:
        console.print(f"[red]Error loading conversation: {e}[/red]")

    # Return empty list or just system message if load failed
    if system:
        return [{"role": "system", "content": system}]
    return []

