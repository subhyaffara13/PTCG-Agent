
def _is_policy_version_id(s: str) -> bool:
    """Return True if string is a policy version ID (starts with policy_<uuid> prefix)."""
    from litellm.proxy.policy_engine.policy_registry import POLICY_VERSION_ID_PREFIX

    return isinstance(s, str) and s.startswith(POLICY_VERSION_ID_PREFIX)

