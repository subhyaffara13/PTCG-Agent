from typing import Any, Optional

def _polyfill_will_run(
    *,
    context_management_spec: Any,
    drop_params: Optional[bool],
) -> bool:
    """Return True when ``compact_20260112`` will run via the polyfill dispatcher.

    Mirrors the gating in ``_run_polyfill_if_enabled``: an empty spec or
    effective ``drop_params`` short-circuits the polyfill. The pre-processing
    skip only applies when the dispatcher will actually invoke
    ``apply_compact_20260112`` (which has its own compaction-block slicing).
    """
    edits = _normalize_spec_edits(
        context_management_spec=context_management_spec,
        drop_params=drop_params,
    )
    if edits is None:
        return False

    from litellm.llms.anthropic.experimental_pass_through.context_management.constants import (
        COMPACT_EDIT_TYPE,
    )

    return any(
        isinstance(edit, dict) and edit.get("type") == COMPACT_EDIT_TYPE
        for edit in edits
    )

