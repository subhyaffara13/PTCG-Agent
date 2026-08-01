
def _filter_keys_by_created_since(
    source_keys: List[Dict[str, Any]],
    created_since_dt: Optional[datetime],
    created_since: str,
) -> List[Dict[str, Any]]:
    """Filter keys by created_since date if specified."""
    if not created_since_dt:
        return source_keys

    filtered_keys = []
    for key in source_keys:
        key_created_at = key.get("created_at")
        if key_created_at:
            # Parse the key's created_at timestamp
            if isinstance(key_created_at, str):
                if "T" in key_created_at:
                    key_dt = datetime.fromisoformat(
                        key_created_at.replace("Z", "+00:00")
                    )
                else:
                    key_dt = datetime.fromisoformat(key_created_at)

                # Convert to naive datetime for comparison (assuming UTC)
                if key_dt.tzinfo:
                    key_dt = key_dt.replace(tzinfo=None)

                if key_dt >= created_since_dt:
                    filtered_keys.append(key)

    click.echo(
        f"Filtered {len(source_keys)} keys to {len(filtered_keys)} keys created since {created_since}"
    )
    return filtered_keys

