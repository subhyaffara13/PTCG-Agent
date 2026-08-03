from typing import Any, Dict, List, Optional

def _select_model(
    console: Console, available_models: List[Dict[str, Any]]
) -> Optional[str]:
    """Interactive model selection"""
    if not available_models:
        console.print(
            "[yellow]No models available or could not fetch models list.[/yellow]"
        )
        model_name = Prompt.ask("Please enter a model name")
        return model_name if model_name.strip() else None

    # Display available models in a table
    table = Table(title="Available Models")
    table.add_column("Index", style="cyan", no_wrap=True)
    table.add_column("Model ID", style="green")
    table.add_column("Owned By", style="yellow")
    MAX_MODELS_TO_DISPLAY = 200

    models_to_display: List[Dict[str, Any]] = available_models[:MAX_MODELS_TO_DISPLAY]
    for i, model in enumerate(models_to_display):  # Limit to first 200 models
        table.add_row(
            str(i + 1), str(model.get("id", "")), str(model.get("owned_by", ""))
        )

    if len(available_models) > MAX_MODELS_TO_DISPLAY:
        console.print(
            f"\n[dim]... and {len(available_models) - MAX_MODELS_TO_DISPLAY} more models[/dim]"
        )

    console.print(table)

    while True:
        try:
            choice = Prompt.ask(
                "\nSelect a model by entering the index number (or type a model name directly)",
                default="1",
            ).strip()

            # Try to parse as index
            try:
                index = int(choice) - 1
                if 0 <= index < len(available_models):
                    return available_models[index]["id"]
                else:
                    console.print(
                        f"[red]Invalid index. Please enter a number between 1 and {len(available_models)}[/red]"
                    )
                    continue
            except ValueError:
                # Not a number, treat as model name
                if choice:
                    return choice
                else:
                    console.print("[red]Please enter a valid model name or index[/red]")
                    continue

        except KeyboardInterrupt:
            console.print("\n[yellow]Model selection cancelled.[/yellow]")
            return None

