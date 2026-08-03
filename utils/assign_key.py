from typing import Optional

def assign_key(ctx: click.Context, team_id: Optional[str]):
    """Assign your current CLI key to a team"""
    client = Client(ctx.obj["base_url"], ctx.obj["api_key"])
    api_key = ctx.obj["api_key"]

    if not api_key:
        click.echo("❌ No API key found. Please login first using 'litellm login'")
        raise click.Abort()

    try:
        # If no team_id provided, show teams and let user select
        if not team_id:
            teams = client.teams.list()

            if not teams:
                click.echo("❌ No teams found for your user.")
                return

            # Use interactive selection from auth module
            from .auth import prompt_team_selection

            selected_team = prompt_team_selection(teams)

            if selected_team:
                team_id = selected_team.get("team_id")
            else:
                click.echo("❌ Operation cancelled.")
                return

        # Update the key with the selected team
        if team_id:
            click.echo(f"\n🔄 Assigning your key to team: {team_id}")
            client.keys.update(key=api_key, team_id=team_id)
            click.echo(f"✅ Successfully assigned key to team: {team_id}")

            # Show team details if available
            teams = client.teams.list()
            for team in teams:
                if team.get("team_id") == team_id:
                    models = team.get("models", [])
                    if models:
                        click.echo(f"🎯 You can now access models: {', '.join(models)}")
                    else:
                        click.echo("🎯 You can now access all available models")
                    break

    except requests.exceptions.HTTPError as e:
        click.echo(f"Error: HTTP {e.response.status_code}", err=True)
        error_body = e.response.json()
        click.echo(f"Details: {error_body.get('detail', 'Unknown error')}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

