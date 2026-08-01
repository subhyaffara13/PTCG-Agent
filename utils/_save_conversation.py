
def _save_conversation(console: Console, messages: List[Dict[str, Any]], command: str):
    """Save conversation to a file"""
    parts = command.split()
    if len(parts) < 2:
        console.print("[red]Usage: /save <filename>[/red]")
        return

    filename = parts[1]
    if not filename.endswith(".json"):
        filename += ".json"

    try:
        with open(filename, "w") as f:
            json.dump(messages, f, indent=2)
        console.print(f"[green]Conversation saved to {filename}[/green]")
    except Exception as e:
        console.print(f"[red]Error saving conversation: {e}[/red]")

