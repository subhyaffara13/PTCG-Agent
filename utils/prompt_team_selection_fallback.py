from typing import Any, Dict, List, Optional

def prompt_team_selection_fallback(
    teams: List[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """Fallback team selection for non-interactive environments"""
    if not teams:
        return None

    while True:
        try:
            choice = click.prompt(
                "\nSelect a team by entering the index number (or 'skip' to continue without a team)",
                type=str,
            ).strip()

            if choice.lower() == "skip":
                return None

            index = int(choice) - 1
            if 0 <= index < len(teams):
                selected_team = teams[index]
                click.echo(
                    f"\n✅ Selected team: {selected_team.get('team_alias', 'N/A')} ({selected_team.get('team_id')})"
                )
                return selected_team
            else:
                click.echo(
                    f"❌ Invalid selection. Please enter a number between 1 and {len(teams)}"
                )
        except ValueError:
            click.echo("❌ Invalid input. Please enter a number or 'skip'")
        except KeyboardInterrupt:
            click.echo("\n❌ Team selection cancelled.")
            return None

