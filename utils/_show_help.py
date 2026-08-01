
def _show_help(console: Console):
    """Show help for interactive chat commands"""
    help_text = """
[bold]Interactive Chat Commands:[/bold]

[cyan]/help[/cyan]     - Show this help message
[cyan]/quit[/cyan]     - Exit the chat session (also /exit, /q)
[cyan]/clear[/cyan]    - Clear conversation history
[cyan]/history[/cyan]  - Show conversation history
[cyan]/model[/cyan]    - Switch to a different model
[cyan]/save <name>[/cyan] - Save conversation to file
[cyan]/load <name>[/cyan] - Load conversation from file

[bold]Tips:[/bold]
- Your conversation history is maintained during the session
- Use Ctrl+C to interrupt at any time
- Responses are streamed in real-time
- You can switch models mid-conversation with /model
    """
    console.print(Panel(help_text, title="Help"))

