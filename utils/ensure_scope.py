
def ensure_scope(
    level: int, global_dict=None, local_dict=None, resolvers=(), target=None
) -> Scope:
    """Ensure that we are grabbing the correct scope."""
    return Scope(
        level + 1,
        global_dict=global_dict,
        local_dict=local_dict,
        resolvers=resolvers,
        target=target,
    )

