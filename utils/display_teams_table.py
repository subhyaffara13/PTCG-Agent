from typing import Any, Dict, List

def display_teams_table(teams: List[Dict[str, Any]]) -> None:
    """Display teams in a formatted table"""
    console = Console()

    if not teams:
        console.print("❌ No teams found for your user.")
        return

    table = Table(title="Available Teams")
    table.add_column("Index", style="cyan", no_wrap=True)
    table.add_column("Team Alias", style="magenta")
    table.add_column("Team ID", style="green")
    table.add_column("Models", style="yellow")
    table.add_column("Max Budget", style="blue")

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

        table.add_row(str(i + 1), team_alias, team_id, models_str, budget_str)

    console.print(table)


def display_teams_table(teams: List[Dict[str, Any]]) -> None:
    """Display teams in a formatted table"""
    console = Console()

    if not teams:
        console.print("❌ No teams found for your user.")
        return

    table = Table(title="Available Teams")
    table.add_column("Index", style="cyan", no_wrap=True)
    table.add_column("Team Alias", style="magenta")
    table.add_column("Team ID", style="green")
    table.add_column("Models", style="yellow")
    table.add_column("Max Budget", style="blue")
    table.add_column("Role", style="red")

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

        # Try to determine role (this might vary based on API response structure)
        role = "Member"  # Default role
        if (
            isinstance(team, dict)
            and "members_with_roles" in team
            and team["members_with_roles"]
        ):
            # This would need to be implemented based on actual API response structure
            pass

        table.add_row(str(i + 1), team_alias, team_id, models_str, budget_str, role)

    console.print(table)

