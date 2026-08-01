
def _extract_policy_id(s: str) -> Optional[str]:
    """Extract raw UUID from policy_<uuid> string, or None if not a valid version ID."""
    from litellm.proxy.policy_engine.policy_registry import POLICY_VERSION_ID_PREFIX

    if not _is_policy_version_id(s):
        return None
    return s[len(POLICY_VERSION_ID_PREFIX) :].strip() or None

