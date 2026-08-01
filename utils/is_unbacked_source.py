
def is_unbacked_source(source_name: str) -> bool:
    unbacked_sources = get_unbacked_sources()
    for pattern in unbacked_sources:
        if pattern == source_name or re.match(pattern, source_name):
            log.debug(
                "%s was marked unbacked due to unbacked source allowlist pattern: %s",
                source_name,
                pattern,
            )
            return True
    return False

