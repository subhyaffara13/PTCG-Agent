
def isfilelike(f: Any) -> TypeGuard[IO[bytes]]:
    return all(hasattr(f, attr) for attr in ["read", "close", "tell"])

