
def _isolation_key(ischema: IsolationSchema = _DEFAULT_ISOLATION_SCHEMA) -> str:
    """Generate a unique key for the given isolation schema.

    Args:
        ischema: Schema specifying which context forms to include.
                Defaults to including all runtime and compile context.

    Returns:
        A 32-character hexadecimal string that uniquely identifies
        the context specified by the isolation schema.
    """
    return sha256(
        json.dumps(_isolation_context(ischema), sort_keys=True).encode()
    ).hexdigest()[:32]

