
def _handle_special_commands(
    console: Console,
    user_input: str,
    messages: List[Dict[str, Any]],
    system: Optional[str],
    ctx: click.Context,
) -> tuple[bool, List[Dict[str, Any]], Optional[str]]:
    """Handle special chat commands. Returns (should_exit, updated_messages, updated_model)"""
    if user_input.lower() in ["/quit", "/exit", "/q"]:
        console.print("[yellow]Chat session ended.[/yellow]")
        return True, messages, None
    elif user_input.lower() == "/help":
        _show_help(console)
        return False, messages, None
    elif user_input.lower() == "/clear":
        new_messages = []
        if system:
            new_messages.append({"role": "system", "content": system})
        console.print("[green]Conversation history cleared.[/green]")
        return False, new_messages, None
    elif user_input.lower() == "/history":
        _show_history(console, messages)
        return False, messages, None
    elif user_input.lower().startswith("/save"):
        _save_conversation(console, messages, user_input)
        return False, messages, None
    elif user_input.lower().startswith("/load"):
        new_messages = _load_conversation(console, user_input, system)
        return False, new_messages, None
    elif user_input.lower() == "/model":
        available_models = _get_available_models(ctx)
        new_model = _select_model(console, available_models)
        if new_model:
            console.print(f"[green]Switched to model: {new_model}[/green]")
            return False, messages, new_model
        return False, messages, None
    elif not user_input:
        return False, messages, None

    # Not a special command
    return False, messages, None

