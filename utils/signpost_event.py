
def signpost_event(category: str, name: str, parameters: dict[str, Any]):
    log.info("%s %s: %r", category, name, parameters)

