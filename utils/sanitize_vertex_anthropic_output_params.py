
def sanitize_vertex_anthropic_output_params(data: dict, model: str) -> None:
    """
    Strip Vertex-unsupported keys from ``output_config`` /
    ``output_format`` in-place; forward whatever remains.

    Behavior:
      * ``output_config.effort`` is dropped for models that don't accept it
        (e.g. Haiku 4.5) and forwarded for those that do (Opus/Sonnet 4.6+).
        Clients like Claude Code inject it into every Messages payload, so the
        gate has to live here rather than rely on the caller.
      * Keys in ``VERTEX_UNSUPPORTED_OUTPUT_CONFIG_KEYS`` are always filtered.
      * ``output_config`` left empty after filtering is removed so the request
        body has no empty dict.
      * ``output_format`` is forwarded as-is (Vertex AI Claude accepts it).
      * Non-dict values for ``output_config`` are dropped to avoid sending
        malformed payloads downstream.
    """
    output_config = data.get("output_config")
    if output_config is None:
        return
    if not isinstance(output_config, dict):
        data.pop("output_config", None)
        return

    drop_keys = set(VERTEX_UNSUPPORTED_OUTPUT_CONFIG_KEYS)
    if "effort" in output_config and not _model_accepts_output_config_effort(model):
        from litellm._logging import verbose_logger

        verbose_logger.debug(
            "Dropping unsupported output_config.effort for vertex_ai model=%s "
            "(no supports_output_config in the model map)",
            model,
        )
        drop_keys.add("effort")

    sanitized = {k: v for k, v in output_config.items() if k not in drop_keys}
    if sanitized:
        data["output_config"] = sanitized
    else:
        data.pop("output_config", None)

