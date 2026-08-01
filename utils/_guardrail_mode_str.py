
def _guardrail_mode_str(value: object) -> str | None:
    """Normalize ``guardrail_mode`` to a stable string.

    ``guardrail_mode`` is typed as a ``GuardrailEventHooks`` enum, a list of them,
    or a ``GuardrailMode`` — not a plain string. Emit the enum *value* (e.g.
    ``"pre_call"``) rather than ``str(enum)`` (``"GuardrailEventHooks.pre_call"``),
    and join a list of modes so a guardrail that runs at multiple hooks is
    represented faithfully.
    """
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        parts: list[str] = []
        for item in value:
            if item is None:
                continue
            part = as_str(item.value) if isinstance(item, Enum) else as_str(item)
            if part:
                parts.append(part)
        return ",".join(parts) or None
    if isinstance(value, Enum):
        return as_str(value.value)
    return as_str(value)

