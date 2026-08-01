
def log_input(name: str, var: object) -> None:
    logger.info("input", (name,), {}, var)  # noqa: PLE1205

