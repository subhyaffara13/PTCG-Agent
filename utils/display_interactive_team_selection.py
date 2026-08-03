from typing import Any, Dict, List

def display_interactive_team_selection(
    teams: List[Dict[str, Any]], selected_index: int = 0
) -> None:
    """Display teams with one highlighted for selection"""
    console = Console()

    # Clear the screen using Rich's method
    console.clear()

    console.print("🎯 Select a Team (Use ↑↓ arrows, Enter to select, 'q' to skip):\n")

    for i, team in enumerate(teams):
        team_alias = team.get("team_alias") or "N/A"
        team_id = team.get("team_id", "N/A")
        models = team.get("models", [])
        max_budget = team.get("max_budget")

        # Format models list
        if models:
            if len(models) > 3:
                models_str = ", ".join(models[:3]) + f" (+{len(models) - 3} more)"
            else:
                models_str = ", ".join(models)
        else:
            models_str = "All models"

        # Format budget
        budget_str = f"${max_budget}" if max_budget else "Unlimited"

        # Highlight the selected item
        if i == selected_index:
            console.print(f"➤ [bold cyan]{team_alias}[/bold cyan] ({team_id})")
            console.print(f"   Models: [yellow]{models_str}[/yellow]")
            console.print(f"   Budget: [blue]{budget_str}[/blue]\n")
        else:
            console.print(f"  [dim]{team_alias}[/dim] ({team_id})")
            console.print(f"   Models: [dim]{models_str}[/dim]")
            console.print(f"   Budget: [dim]{budget_str}[/dim]\n")

