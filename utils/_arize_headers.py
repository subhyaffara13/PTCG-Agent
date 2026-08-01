
def _arize_headers(arize_cfg) -> str | None:
    pieces = []
    if arize_cfg.space_id or arize_cfg.space_key:
        pieces.append(f"space_id={arize_cfg.space_id or arize_cfg.space_key}")
    if arize_cfg.api_key:
        pieces.append(f"api_key={arize_cfg.api_key}")
    if not pieces:
        # Fall back to the standard OTLP headers env var when no Arize
        # credentials are configured.
        return _ArizeSettings().otlp_traces_headers
    return ",".join(pieces)

