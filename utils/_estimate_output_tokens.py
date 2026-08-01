
def _estimate_output_tokens(
    request_body: dict,
    route: str,
    model_info: Dict[str, Any],
) -> Optional[int]:
    if _is_input_only_route(route=route):
        return 0

    requested: Optional[int] = None
    for key in ("max_completion_tokens", "max_tokens", "max_output_tokens"):
        requested = _to_int(request_body.get(key))
        if requested is not None:
            break

    # Clamp at min(requested-or-default, model_max-or-default). Two purposes:
    # (1) Without an explicit cap we still need a finite reservation so the
    #     atomic admission counter actually bounds concurrent in-flight cost
    #     (mirrors parallel_request_limiter_v3's DEFAULT_MAX_TOKENS_ESTIMATE).
    # (2) An adversarial caller cannot send max_tokens=999999999 to inflate
    #     the reservation up to remaining team headroom and pin the counter
    #     at the cap — the model can only physically emit max_output_tokens
    #     anyway, so reserving more is both wasteful and a DoS surface.
    model_ceiling = (
        _to_int(model_info.get("max_output_tokens"))
        or DEFAULT_MAX_OUTPUT_TOKENS_FALLBACK
    )
    if requested is None:
        requested = DEFAULT_MAX_OUTPUT_TOKENS_FALLBACK
    return min(requested, model_ceiling)

