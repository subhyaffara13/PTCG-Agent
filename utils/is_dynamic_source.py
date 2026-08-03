import re

def is_dynamic_source(source_name: str) -> bool:
    dynamic_sources = get_dynamic_sources()
    for pattern in dynamic_sources:
        if pattern == source_name or re.match(pattern, source_name):
            log.debug(
                "%s was marked dynamic due to dynamic source allowlist pattern: %s",
                source_name,
                pattern,
            )
            return True
    return False

