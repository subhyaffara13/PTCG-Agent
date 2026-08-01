
def available(ctx: click.Context):
    """List teams that are available to join"""
    client = Client(ctx.obj["base_url"], ctx.obj["api_key"])

    try:
        teams = client.teams.get_available()
        if teams:
            console = Console()
            console.print("\n🎯 Available Teams to Join:")
            display_teams_table(teams)
        else:
            click.echo("ℹ️ No available teams to join.")
    except requests.exceptions.HTTPError as e:
        click.echo(f"Error: HTTP {e.response.status_code}", err=True)
        error_body = e.response.json()
        click.echo(f"Details: {error_body.get('detail', 'Unknown error')}", err=True)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

