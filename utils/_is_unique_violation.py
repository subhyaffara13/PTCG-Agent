
def _is_unique_violation(exc: Exception) -> bool:
    """
    Detect a Prisma unique-constraint violation.

    Prefer the typed error code `P2002` from `PrismaClientKnownRequestError`;
    fall back to string matching so we stay robust across Prisma versions
    where the typed class may be unavailable or differently named.
    """
    code = getattr(exc, "code", None)
    if code == "P2002":
        return True
    msg = str(exc)
    return (
        "P2002" in msg or "Unique" in msg or "unique" in msg or "UniqueViolation" in msg
    )

