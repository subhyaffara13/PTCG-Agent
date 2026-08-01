
def show_commands():
    """Display available commands."""
    from .commands.agents import agent_commands

    commands = [
        ("login", "Authenticate with the LiteLLM proxy server"),
        ("logout", "Clear stored authentication"),
        ("whoami", "Show current authentication status"),
        ("models", "Manage and view model configurations"),
        ("credentials", "Manage API credentials"),
        ("chat", "Interactive streaming chat with models"),
        ("http", "Make HTTP requests to the proxy"),
        ("keys", "Manage API keys"),
        ("teams", "Manage teams and team assignments"),
        ("users", "Manage users"),
    ]
    commands += [(c.name, c.get_short_help_str()) for c in agent_commands()]
    commands += [
        ("version", "Show version information"),
        ("help", "Show this help message"),
        ("quit", "Exit the interactive session"),
    ]

    click.echo("Available commands:")
    for cmd, description in commands:
        click.echo(f"  {cmd:<20} {description}")
    click.echo()

