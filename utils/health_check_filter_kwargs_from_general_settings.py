
def health_check_filter_kwargs_from_general_settings(
    general_settings: Optional[dict],
) -> dict:
    """
    Build kwargs for ``perform_health_check`` from ``general_settings``.

    When ``health_check_skip_disabled_background_models`` is true, deployments with
    ``model_info.disable_background_health_check`` are omitted from health runs
    (including on-demand ``GET /health``), matching the background loop behavior.
    """
    g = general_settings or {}
    return {
        "health_check_skip_disabled_background_models": bool(
            g.get("health_check_skip_disabled_background_models", False)
        ),
    }

