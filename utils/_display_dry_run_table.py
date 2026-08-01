
def _display_dry_run_table(source_keys: List[Dict[str, Any]]) -> None:
    """Display a table of keys that would be imported in dry-run mode."""
    click.echo("\n--- DRY RUN MODE ---")
    table = Table(title="Keys that would be imported")
    table.add_column("Key Alias", style="green")
    table.add_column("User ID", style="magenta")
    table.add_column("Created", style="cyan")

    for key in source_keys:
        created_at = key.get("created_at", "")
        # Format the timestamp if it exists
        if created_at:
            # Try to parse and format the timestamp for better readability
            if isinstance(created_at, str):
                # Handle common timestamp formats
                if "T" in created_at:
                    dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    created_at = dt.strftime("%Y-%m-%d %H:%M")

        table.add_row(
            str(key.get("key_alias", "")), str(key.get("user_id", "")), str(created_at)
        )
    rich.print(table)

