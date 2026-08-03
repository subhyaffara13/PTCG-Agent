from typing import Any

def _team_metadata_dict(value: object) -> Mapping[str, Any] | None:
    """The team's free-form metadata as a raw mapping, or ``None`` when missing
    or empty.

    Carried raw on the identity and filtered to an operator allowlist only at
    Baggage-promotion time (see ``baggage.promoted_baggage``), so an empty case
    is dropped rather than carrying a useless ``{}``.
    """
    if isinstance(value, Mapping) and value:
        return dict(value)
    return None

