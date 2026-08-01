
def _build_db_connection_url_params(
    connection_limit: int,
    pool_timeout: Optional[Union[int, float]],
    connect_timeout: Optional[Union[int, float]] = None,
    socket_timeout: Optional[Union[int, float]] = None,
    disable_prepared_statements: bool = False,
    extra_params: Optional[dict] = None,
) -> dict:
    """Build the Prisma DATABASE_URL query params controlling connection pool behavior.

    `connect_timeout` / `socket_timeout` map to the Prisma URL params of the same
    name (https://www.prisma.io/docs/orm/overview/databases/postgresql) and are
    omitted when None so Prisma's defaults apply. `disable_prepared_statements`
    sets `pgbouncer=true`, which makes Prisma stop using server-side prepared
    statements (pgbouncer transaction-pool compatible; also sidesteps the
    "cached plan must not change result type" error during rolling migrations).
    `extra_params` is an untyped passthrough — keys it provides win over the
    named arguments above, so it can be used to override any default we set here.
    """
    params: dict = {
        "connection_limit": connection_limit,
    }
    if pool_timeout is not None:
        params["pool_timeout"] = pool_timeout
    if connect_timeout is not None:
        params["connect_timeout"] = connect_timeout
    if socket_timeout is not None:
        params["socket_timeout"] = socket_timeout
    if disable_prepared_statements:
        params["pgbouncer"] = "true"
    if extra_params:
        params.update(extra_params)
    return params

