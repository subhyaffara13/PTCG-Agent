
def _redact_config(config: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    """Strip values from a config snapshot before audit-log emission.

    Hashicorp Vault config carries ``vault_token``, ``approle_secret_id``,
    ``client_key`` etc.  Persisting them verbatim into ``LiteLLM_AuditLogs``
    would let anyone with read access to the audit table harvest the
    proxy's KMS credentials.  Keep keys, redact values.
    """
    if not config:
        return {}
    return {k: _AUDIT_REDACTED for k in config.keys()}

