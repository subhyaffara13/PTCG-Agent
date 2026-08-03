from typing import Any

def _add_attrs(
    token: Token,
    attrs: dict[str, Any],
    allowed: set[str] | None,
) -> None:
    """Add attributes to a token, skipping any disallowed attributes."""
    if allowed is not None and (
        disallowed := {k: v for k, v in attrs.items() if k not in allowed}
    ):
        token.meta["insecure_attrs"] = disallowed
        attrs = {k: v for k, v in attrs.items() if k in allowed}

    # attributes takes precedence over existing attributes
    token.attrs.update(attrs)

