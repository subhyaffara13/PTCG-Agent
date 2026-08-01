
def ignore_conflicts(
    namespace: str, name: str, entrypoints: list[Extension[T]]
) -> Extension[T]:
    LOG.warning(
        "multiple implementations found for the '%(name)s' extension in "
        "%(namespace)s namespace: %(conflicts)s",
        {
            'name': name,
            'namespace': namespace,
            'conflicts': ', '.join(
                ep.plugin.__qualname__ for ep in entrypoints
            ),
        },
    )
    # use the most last found entrypoint
    return entrypoints[-1]

