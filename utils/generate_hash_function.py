
def generate_hash_function(frozen: bool) -> Optional[Callable[[Any], int]]:
    def hash_function(self_: Any) -> int:
        return hash(self_.__class__) + hash(tuple(self_.__dict__.values()))

    return hash_function if frozen else None

