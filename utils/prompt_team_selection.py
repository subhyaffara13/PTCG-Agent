import sys
from typing import Any, Dict, List, Optional

def prompt_team_selection(teams: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Interactive team selection with arrow keys"""
    if not teams:
        return None

    selected_index = 0

    try:
        # Check if we can use interactive mode
        if not sys.stdin.isatty():
            # Fallback to simple selection for non-interactive environments
            return prompt_team_selection_fallback(teams)

        while True:
            display_interactive_team_selection(teams, selected_index)

            key = get_key_input()

            if key == "up":
                selected_index = (selected_index - 1) % len(teams)
            elif key == "down":
                selected_index = (selected_index + 1) % len(teams)
            elif key == "enter":
                selected_team = teams[selected_index]
                # Clear screen and show selection
                console = Console()
                console.clear()
                click.echo(
                    f"✅ Selected team: {selected_team.get('team_alias', 'N/A')} ({selected_team.get('team_id')})"
                )
                return selected_team
            elif key == "quit" or key == "escape":
                # Clear screen
                console = Console()
                console.clear()
                click.echo("ℹ️ Team selection skipped.")
                return None
            elif key is None:
                # If we can't get key input, fall back to simple selection
                return prompt_team_selection_fallback(teams)

    except KeyboardInterrupt:
        console = Console()
        console.clear()
        click.echo("\n❌ Team selection cancelled.")
        return None
    except Exception:
        # If interactive mode fails, fall back to simple selection
        return prompt_team_selection_fallback(teams)

