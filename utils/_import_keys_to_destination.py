
def _import_keys_to_destination(
    source_keys: List[Dict[str, Any]], dest_client: KeysManagementClient
) -> tuple[int, int]:
    """Import each key to the destination instance and return counts."""
    imported_count = 0
    failed_count = 0

    for key in source_keys:
        try:
            # Prepare key data for import
            import_data = _prepare_key_import_data(key)

            # Generate the key in destination instance
            response = dest_client.generate(**import_data)
            click.echo(f"Generated key: {response}")
            # The generate method returns JSON data directly, not a Response object
            imported_count += 1

            key_alias = key.get("key_alias", "N/A")
            click.echo(f"✓ Imported key: {key_alias}")

        except Exception as e:
            failed_count += 1
            key_alias = key.get("key_alias", "N/A")
            click.echo(f"✗ Failed to import key {key_alias}: {str(e)}", err=True)

    return imported_count, failed_count

