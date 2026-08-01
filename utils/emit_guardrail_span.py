
def emit_guardrail_span(entry: "StandardLoggingGuardrailInformation") -> None:
    """Emit a guardrail span on the registered v2 OTel logger.

    Called by the guardrail-recording code the moment a guardrail finishes, so a
    span is produced regardless of whether a post-call hook later runs (it does
    not on the pass-through allow path). Routes through the single canonical
    logger — the same one every other v2 entry point uses — so a guardrail
    recorded once yields exactly one span; fanning out across every reachable
    ``OpenTelemetryV2`` instance double-emits the same entry. Best-effort: span
    emission must never break guardrail evaluation.
    """
    logger = _registered_v2_logger()
    if logger is None:
        return
    try:
        logger.emit_guardrail_span(entry)
    except Exception:
        pass

