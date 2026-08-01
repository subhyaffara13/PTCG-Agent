
def _get_bundled_model_cost_map() -> Dict[str, Any]:
    try:
        model_cost_path = resources.files("litellm").joinpath(
            "model_prices_and_context_window_backup.json"
        )
        return json.loads(model_cost_path.read_text())
    except Exception:
        return {}

