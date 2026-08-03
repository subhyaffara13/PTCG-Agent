from typing import Dict, List

def resolve_credentials(sources: List[Source]) -> Dict[str, str]:
    """Extract credentials from the first source that has any defined."""
    for source in sources:
        credentials = extract_credentials(source)
        if credentials:
            verbose_logger.debug(f"Resolved SAP credentials from source {source.name}")
            return credentials
    raise ValueError("No credentials found in any source")

