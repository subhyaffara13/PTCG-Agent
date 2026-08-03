from typing import List, Optional

def resolve_resource_group(sources: List[Source]) -> Optional[str]:
    """Find resource_group from the first source that defines it."""
    rg_cred = CredentialsValue("resource_group", default="default")
    for source in sources:
        value = source.get(rg_cred)
        if value is not None:
            verbose_logger.debug(
                f"Resolved GEN AI Hub resource_group from source {source.name}"
            )
            return value
    return rg_cred.default

