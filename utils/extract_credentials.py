from typing import Dict

def extract_credentials(source: Source) -> Dict[str, str]:
    """Extract all credentials from a source."""
    credentials = {}
    for cv in CREDENTIAL_VALUES:
        value = source.get(cv)
        if value is not None:
            credentials[cv.name] = cv.transform_fn(value) if cv.transform_fn else value
    return credentials

