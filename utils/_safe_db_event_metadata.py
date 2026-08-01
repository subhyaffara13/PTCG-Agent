
def _safe_db_event_metadata(kwargs: Dict) -> Optional[Dict[str, str]]:
    """Minimal, non-sensitive ``event_metadata`` for a DB service log.

    The raw ``kwargs``/``args`` carry live objects (Prisma client, OTel spans)
    and secrets (tokens), none of which belongs on a span — so we surface only
    the table name when present. Everything else is dropped.
    """
    table_name = kwargs.get("table_name")
    return {"table_name": table_name} if isinstance(table_name, str) else None

