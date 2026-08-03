from typing import Any, Dict, List, Optional

def _render_and_prompt_for_team_selection(teams: List[Dict[str, Any]]) -> Optional[str]:
    """Render teams table and prompt user for a team selection.

    Returns the selected team_id as a string, or None if selection was
    cancelled or skipped without any teams available.
    """
    # Display teams as a simple list, but prefer showing aliases where
    # available while still keeping the underlying IDs intact.
    console = Console()
    table = Table(title="Available Teams")
    table.add_column("Index", style="cyan", no_wrap=True)
    table.add_column("Team Name", style="magenta")
    table.add_column("Team ID", style="green")

    for i, team in enumerate(teams):
        team_id = str(team.get("team_id"))
        team_alias = team.get("team_alias") or team_id
        table.add_row(str(i + 1), team_alias, team_id)

    console.print(table)

    # Simple selection
    while True:
        try:
            choice = click.prompt(
                "\nSelect a team by entering the index number (or 'skip' to use first team)",
                type=str,
            ).strip()

            if choice.lower() == "skip":
                # Default to the first team's ID if the user skips an
                # explicit selection.
                if teams:
                    first_team = teams[0]
                    return str(first_team.get("team_id"))
                return None

            index = int(choice) - 1
            if 0 <= index < len(teams):
                selected_team = teams[index]
                team_id = str(selected_team.get("team_id"))
                team_alias = selected_team.get("team_alias") or team_id
                click.echo(f"\n✅ Selected team: {team_alias} ({team_id})")
                return team_id

            click.echo(
                f"❌ Invalid selection. Please enter a number between 1 and {len(teams)}"
            )
        except ValueError:
            click.echo("❌ Invalid input. Please enter a number or 'skip'")
        except KeyboardInterrupt:
            click.echo("\n❌ Team selection cancelled.")
            return None

