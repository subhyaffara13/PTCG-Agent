
def _show_history(console: Console, messages: List[Dict[str, Any]]):
    """Show conversation history"""
    if not messages:
        console.print("[yellow]No conversation history.[/yellow]")
        return

    console.print(Panel.fit("[bold]Conversation History[/bold]", title="History"))

    for i, message in enumerate(messages, 1):
        role = message["role"]
        content = message["content"]

        if role == "system":
            console.print(
                f"[dim]{i}. [bold magenta]System:[/bold magenta] {content}[/dim]"
            )
        elif role == "user":
            console.print(f"{i}. [bold cyan]You:[/bold cyan] {content}")
        elif role == "assistant":
            console.print(
                f"{i}. [bold green]Assistant:[/bold green] {content[:100]}{'...' if len(content) > 100 else ''}"
            )

