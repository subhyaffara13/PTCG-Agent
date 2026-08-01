
def _parse_created_since_filter(created_since: Optional[str]) -> Optional[datetime]:
    """Parse and validate the created_since date filter."""
    if not created_since:
        return None

    try:
        # Support formats: YYYY-MM-DD_HH:MM or YYYY-MM-DD
        if "_" in created_since:
            return datetime.strptime(created_since, "%Y-%m-%d_%H:%M")
        else:
            return datetime.strptime(created_since, "%Y-%m-%d")
    except ValueError:
        click.echo(
            f"Error: Invalid date format '{created_since}'. Use YYYY-MM-DD_HH:MM or YYYY-MM-DD",
            err=True,
        )
        raise click.Abort()

