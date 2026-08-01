
def _handle_team_selection_during_polling(
    base_url: str, key_id: str, poll_secret: str, teams: List[Dict[str, Any]]
) -> Optional[str]:
    """
    Handle team selection and re-poll with selected team_id.

    Args:
        teams: List of team IDs (strings)

    Returns:
        The JWT token with the selected team, or None if selection was skipped
    """
    if not teams:
        click.echo(
            "ℹ️ No teams found. You can create or join teams using the web interface."
        )
        return None

    click.echo("\n" + "=" * 60)
    click.echo("📋 Select a team for your CLI session...")

    team_id = _render_and_prompt_for_team_selection(teams)

    if not team_id:
        click.echo("ℹ️ No team selected.")
        return None

    click.echo(f"\n🔄 Generating JWT for team: {team_id}")

    poll_url = f"{base_url}/sso/cli/poll/{key_id}?team_id={team_id}"
    data = _poll_for_ready_data(
        poll_url,
        headers=_get_cli_sso_poll_headers(poll_secret),
        pending_message="Still waiting for team authentication...",
        other_status_message="Waiting for team authentication to complete...",
        http_error_log_every=10,
    )
    if not data:
        return None
    jwt_token = data.get("key")
    if jwt_token:
        click.echo(f"✅ Successfully generated JWT for team: {team_id}")
        return jwt_token

    return None

