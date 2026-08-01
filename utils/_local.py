
def _local(name: str, config: Config) -> tuple[str, str] | None:
    if name.startswith("."):
        return (LOCAL, "Module name started with a dot.")

    return None

