from typing import Any, Dict, List, Optional, Union

def apply_client_compaction_block_history(
    *,
    messages: List[Dict[str, Any]],
    system: Optional[Union[str, List[Dict[str, Any]]]],
) -> Optional[PolyfillResult]:
    """Honor client-sent compaction blocks without a ``compact_20260112`` edit.

    When the request omits ``context_management`` but the message history already
    contains a ``compaction`` content block (e.g. Claude Code client-side
    compaction), apply the same slice-only forwarding as the under-threshold
    path: the prior summary is prepended to ``system`` and the post-compaction
    tail is forwarded unchanged (with compaction blocks stripped) so recent
    turns the summary does not cover are preserved.
    """
    effective_messages, prior_compaction_block = _slice_around_compaction_block(
        messages
    )
    if prior_compaction_block is None:
        return None

    verbose_logger.info(
        "compact_20260112: client compaction block in message history; "
        "applying slice-only forwarding (no context_management edit)"
    )

    prior_summary_text = prior_compaction_block.get("content") or ""
    augmented_system: Union[str, List[Dict[str, Any]], None] = system
    if isinstance(prior_summary_text, str) and prior_summary_text:
        augmented_system = _augment_system_with_summary(system, prior_summary_text)
        verbose_logger.info(
            "compact_20260112: compaction summary added to main call system prefix (%s chars)",
            len(prior_summary_text),
        )

    # Post-compaction turns are recent context the prior summary does not cover,
    # so forward them unchanged. Only fall back to the last user question if the
    # strip leaves the downstream call with nothing to answer.
    downstream_messages = _strip_compaction_blocks(effective_messages)
    if not downstream_messages:
        downstream_messages = _select_last_user_question(effective_messages)

    return PolyfillResult(
        messages=downstream_messages,
        system=augmented_system,
        applied_edits=[],
    )

