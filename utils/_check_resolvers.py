
def _check_resolvers(resolvers) -> None:
    if resolvers is not None:
        for resolver in resolvers:
            if not hasattr(resolver, "__getitem__"):
                name = type(resolver).__name__
                raise TypeError(
                    f"Resolver of type '{name}' does not "
                    "implement the __getitem__ method"
                )

