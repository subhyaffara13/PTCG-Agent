
def _normalize_alert_emails(
    cfg: Optional[Dict[str, Any]],
) -> Dict[str, List[str]]:
    """Coerce user-supplied threshold→recipients mapping to Dict[str, List[str]].

    Values may legitimately arrive as list, comma-separated string, or None
    from YAML/metadata; _parse_email_list tolerates all three.
    """
    if not cfg:
        return {}
    return {k: _parse_email_list(v) for k, v in cfg.items()}

