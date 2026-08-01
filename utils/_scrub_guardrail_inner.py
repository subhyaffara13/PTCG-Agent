
def _scrub_guardrail_inner(inner: Dict[str, Any]) -> None:
    """Strip remote-URL entries from a guardrail's ``callbacks`` list
    and ``guardrail`` (v2 module-path) field. Mutates in place."""
    cbs = inner.get("callbacks")
    if isinstance(cbs, list):
        cleaned = [c for c in cbs if not _is_remote_module_url(c)]
        if len(cleaned) != len(cbs):
            verbose_proxy_logger.warning(
                "Refused %d remote-URL entries from DB-overlay "
                "litellm_settings.guardrails[...].callbacks",
                len(cbs) - len(cleaned),
            )
            inner["callbacks"] = cleaned
    if _is_remote_module_url(inner.get("guardrail")):
        verbose_proxy_logger.warning(
            "Refused remote-URL guardrail module from DB-overlay "
            "litellm_settings.guardrails[...].guardrail: %r",
            inner.get("guardrail"),
        )
        inner["guardrail"] = None

