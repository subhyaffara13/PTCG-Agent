
def _select_kept_indices_for_budget(
    normalized_messages: List[dict],
    original_messages: List[dict],
    combined_scores: List[float],
    compression_target: int,
    model: str,
    initial_kept_indices: Set[int],
    tool_exchange_spans: List[Set[int]],
) -> Tuple[Set[int], Dict[int, dict]]:
    kept_indices = set(initial_kept_indices)
    current_tokens = 0
    for i in kept_indices:
        current_tokens += token_counter(
            model=model,
            text=cast(str, normalized_messages[i].get("content", "") or ""),
        )

    # Fill token budget from highest-scoring units.
    # A unit is either:
    # 1) a single message index, or
    # 2) an Anthropic tool-exchange span that must be kept/dropped atomically.
    truncated_overrides: Dict[int, dict] = {}  # idx -> truncated message dict
    span_id_by_index: Dict[int, int] = {}
    for span_id, span in enumerate(tool_exchange_spans):
        for idx in span:
            span_id_by_index[idx] = span_id

    # Build single-message candidate units (non-span messages).
    candidate_units: List[Tuple[float, Tuple[int, ...], bool]] = []
    for idx in range(len(normalized_messages)):
        if idx in span_id_by_index or idx in kept_indices:
            continue
        candidate_units.append((combined_scores[idx], (idx,), True))

    # Build span candidate units (atomic keep/drop for tool exchanges).
    for span in tool_exchange_spans:
        span_indices = tuple(sorted(span))
        if any(idx in kept_indices for idx in span_indices):
            continue
        span_score = max(combined_scores[idx] for idx in span_indices)
        candidate_units.append((span_score, span_indices, False))

    # Sort by descending relevance score.
    candidate_units.sort(key=lambda item: item[0], reverse=True)

    for _score, indices, can_truncate in candidate_units:
        if any(idx in kept_indices for idx in indices):
            continue
        msg_tokens = 0
        for idx in indices:
            msg_tokens += token_counter(
                model=model,
                text=cast(str, normalized_messages[idx].get("content", "") or ""),
            )
        remaining = compression_target - current_tokens

        if remaining <= 0:
            break  # budget exhausted

        if current_tokens + msg_tokens <= compression_target:
            # Fits entirely
            kept_indices.update(indices)
            current_tokens += msg_tokens
        elif can_truncate and len(indices) == 1 and remaining >= 100:
            # Too large to fit whole single message, but we have budget — truncate it.
            idx = indices[0]
            truncated = truncate_message(original_messages[idx], remaining)
            truncated_tokens = token_counter(
                model=model,
                text=truncated.get("content", "") or "",
            )
            truncated_overrides[idx] = truncated
            kept_indices.add(idx)
            current_tokens += truncated_tokens

    return kept_indices, truncated_overrides

