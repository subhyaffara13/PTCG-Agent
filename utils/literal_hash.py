
def literal_hash(e: Expression) -> Key | None:
    """Generate a hashable, (mostly) opaque key for expressions supported by the binder.

    These allow using expressions as dictionary keys based on structural/value
    matching (instead of based on expression identity).

    Return None if the expression type is not supported (it cannot be narrowed).

    See the comment above for more information.

    NOTE: This is not directly related to literal types.
    """
    return e.accept(_hasher)

