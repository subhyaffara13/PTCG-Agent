
def _poll_for_authentication(
    base_url: str, key_id: str, poll_secret: str
) -> Optional[dict]:
    """
    Poll the server for authentication completion and handle team selection.

    Returns:
        Dictionary with authentication data if successful, None otherwise
    """
    poll_url = f"{base_url}/sso/cli/poll/{key_id}"
    data = _poll_for_ready_data(
        poll_url,
        headers=_get_cli_sso_poll_headers(poll_secret),
        pending_message="Still waiting for authentication...",
    )
    if not data:
        return None
    if data.get("requires_team_selection"):
        teams = data.get("teams", [])
        team_details = data.get("team_details")
        user_id = data.get("user_id")
        normalized_teams: List[Dict[str, Any]] = _normalize_teams(teams, team_details)
        if not normalized_teams:
            click.echo("⚠️ No teams available for selection.")
            return None

        # User has multiple teams - let them select
        jwt_with_team = _handle_team_selection_during_polling(
            base_url=base_url,
            key_id=key_id,
            poll_secret=poll_secret,
            teams=normalized_teams,
        )

        # Use the team-specific JWT if selection succeeded
        if jwt_with_team:
            return {
                "api_key": jwt_with_team,
                "user_id": user_id,
                "teams": teams,
                "team_id": None,  # Set by server in JWT
            }

        click.echo("❌ Team selection cancelled or JWT generation failed.")
        return None

    # JWT is ready (single team or team already selected)
    api_key = data.get("key")
    user_id = data.get("user_id")
    teams = data.get("teams", [])
    team_id = data.get("team_id")

    # Show which team was assigned
    if team_id and len(teams) == 1:
        click.echo(f"\n✅ Automatically assigned to team: {team_id}")

    if api_key:
        return {
            "api_key": api_key,
            "user_id": user_id,
            "teams": teams,
            "team_id": team_id,
        }

    return None

