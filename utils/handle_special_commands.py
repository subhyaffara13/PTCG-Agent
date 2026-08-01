
def handle_special_commands(user_input: str) -> bool:
    """Handle special commands like exit, help, clear. Returns True if command was handled."""
    if user_input.lower() in ["exit", "quit"]:
        click.echo("Goodbye!")
        return True
    elif user_input.lower() == "help":
        click.echo("")  # Add space before help
        show_commands()
        return True
    elif user_input.lower() == "clear":
        click.clear()
        from litellm.proxy.common_utils.banner import show_banner

        show_banner()
        show_commands()
        return True

    return False

