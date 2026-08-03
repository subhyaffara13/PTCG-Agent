import json
from typing import Optional

def import_keys(
    ctx: click.Context,
    source_base_url: str,
    source_api_key: Optional[str],
    dry_run: bool,
    created_since: Optional[str],
):
    """Import API keys from another LiteLLM instance"""
    # Parse created_since filter if provided
    created_since_dt = _parse_created_since_filter(created_since)

    # Create clients for both source and destination
    source_client = KeysManagementClient(source_base_url, source_api_key)
    dest_client = KeysManagementClient(ctx.obj["base_url"], ctx.obj["api_key"])

    try:
        # Get all keys from source instance with pagination
        source_keys = _fetch_all_keys_with_pagination(source_client, source_base_url)

        # Filter keys by created_since if specified
        if created_since:
            source_keys = _filter_keys_by_created_since(
                source_keys, created_since_dt, created_since
            )

        if not source_keys:
            click.echo("No keys found in source instance.")
            return

        click.echo(f"Found {len(source_keys)} keys in source instance.")

        if dry_run:
            _display_dry_run_table(source_keys)
            return

        # Import each key
        imported_count, failed_count = _import_keys_to_destination(
            source_keys, dest_client
        )

        # Summary
        click.echo("\nImport completed:")
        click.echo(f"  Successfully imported: {imported_count}")
        click.echo(f"  Failed to import: {failed_count}")
        click.echo(f"  Total keys processed: {len(source_keys)}")

    except requests.exceptions.HTTPError as e:
        click.echo(f"Error: HTTP {e.response.status_code}", err=True)
        try:
            error_body = e.response.json()
            rich.print_json(data=error_body)
        except json.JSONDecodeError:
            click.echo(e.response.text, err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

