from typing import Any, Dict, List, Optional

def chat(
    ctx: click.Context,
    model: Optional[str],
    temperature: float,
    max_tokens: Optional[int] = None,
    system: Optional[str] = None,
):
    """Interactive chat with streaming responses

    Examples:

        # Chat with a specific model
        lite chat gpt-4

        # Chat without specifying model (will show model selection)
        lite chat

        # Chat with custom settings
        lite chat gpt-4 --temperature 0.9 --system "You are a helpful coding assistant"
    """
    console = Console()

    # If no model specified, show model selection
    if not model:
        available_models = _get_available_models(ctx)
        model = _select_model(console, available_models)
        if not model:
            console.print("[red]No model selected. Exiting.[/red]")
            return

    client = ChatClient(ctx.obj["base_url"], ctx.obj["api_key"])

    # Initialize conversation history
    messages: List[Dict[str, Any]] = []

    # Add system message if provided
    if system:
        messages.append({"role": "system", "content": system})

    # Display welcome message
    console.print(
        Panel.fit(
            f"[bold blue]LiteLLM Interactive Chat[/bold blue]\n"
            f"Model: [green]{model}[/green]\n"
            f"Temperature: [yellow]{temperature}[/yellow]\n"
            f"Max Tokens: [yellow]{max_tokens or 'unlimited'}[/yellow]\n\n"
            f"Type your messages and press Enter. Type '/quit' or '/exit' to end the session.\n"
            f"Type '/help' for more commands.",
            title="🤖 Chat Session",
        )
    )

    try:
        while True:
            # Get user input
            try:
                user_input = console.input("\n[bold cyan]You:[/bold cyan] ").strip()
            except (EOFError, KeyboardInterrupt):
                console.print("\n[yellow]Chat session ended.[/yellow]")
                break

            # Handle special commands
            should_exit, messages, new_model = _handle_special_commands(
                console, user_input, messages, system, ctx
            )

            if should_exit:
                break
            if new_model:
                model = new_model

            # Check if this was a special command that was handled (not a normal message)
            if (
                user_input.lower().startswith(
                    (
                        "/quit",
                        "/exit",
                        "/q",
                        "/help",
                        "/clear",
                        "/history",
                        "/save",
                        "/load",
                        "/model",
                    )
                )
                or not user_input
            ):
                continue

            # Add user message to conversation
            messages.append({"role": "user", "content": user_input})

            # Display assistant label
            console.print("\n[bold green]Assistant:[/bold green]")

            # Stream the response
            assistant_content = _stream_response(
                console=console,
                client=client,
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            # Add assistant message to conversation history
            if assistant_content:
                messages.append({"role": "assistant", "content": assistant_content})
            else:
                console.print("[red]Error: No content received from the model[/red]")

    except KeyboardInterrupt:
        console.print("\n[yellow]Chat session interrupted.[/yellow]")

