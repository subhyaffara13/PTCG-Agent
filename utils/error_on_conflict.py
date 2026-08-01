
def error_on_conflict(
    namespace: str, name: str, entrypoints: list[Extension[T]]
) -> Extension[T]:
    raise MultipleMatches(
        "multiple implementations found for the '{name}' command in "
        "{namespace} namespace: {conflicts}".format(
            name=name,
            namespace=namespace,
            conflicts=', '.join(ep.plugin.__qualname__ for ep in entrypoints),
        )
    )

