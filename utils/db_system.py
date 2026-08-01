
def db_system(service_name: str) -> str | None:
    """The ``db.system.name`` for a datastore service, else ``None``.

    ``None`` means the service is not an outbound datastore call. Redis-backed
    spend queues (``redis_*``) map to ``redis``.
    """
    if service_name in _DB_SYSTEM_BY_SERVICE:
        return _DB_SYSTEM_BY_SERVICE[service_name]
    if service_name.startswith("redis_"):
        return "redis"
    return None

