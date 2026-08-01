
def _fetch_all_keys_with_pagination(
    source_client: KeysManagementClient, source_base_url: str
) -> List[Dict[str, Any]]:
    """Fetch all keys from source instance using pagination."""
    click.echo(f"Fetching keys from source server: {source_base_url}")
    source_keys = []
    page = 1
    page_size = 100  # Use a larger page size to minimize API calls

    while True:
        source_response = source_client.list(
            return_full_object=True, page=page, size=page_size
        )
        # source_client.list() returns Dict[str, Any] when return_request is False (default)
        assert isinstance(source_response, dict), "Expected dict response from list API"
        page_keys = source_response.get("keys", [])

        if not page_keys:
            break

        source_keys.extend(page_keys)
        click.echo(f"Fetched page {page}: {len(page_keys)} keys")

        # Check if we got fewer keys than the page size, indicating last page
        if len(page_keys) < page_size:
            break

        page += 1

    return source_keys

