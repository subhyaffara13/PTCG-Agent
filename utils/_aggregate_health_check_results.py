
def _aggregate_health_check_results(
    model_param_to_info: dict,
    healthy_endpoints: list,
    unhealthy_endpoints: list,
) -> dict:
    """
    Aggregate health check results per unique model.

    Uses (model_id, model_name) as key, or (None, model_name) if model_id is None.

    Args:
        model_param_to_info: Mapping from model parameter to model info
        healthy_endpoints: List of healthy endpoint results
        unhealthy_endpoints: List of unhealthy endpoint results

    Returns:
        Dictionary mapping (model_id, model_name) to aggregated health check results
    """
    model_results = {}

    # Process healthy endpoints
    for endpoint in healthy_endpoints:
        model_param = endpoint.get("model")
        if model_param and model_param in model_param_to_info:
            for model_info in model_param_to_info[model_param]:
                key = (model_info["model_id"], model_info["model_name"])
                if key not in model_results:
                    model_results[key] = {
                        "model_name": model_info["model_name"],
                        "model_id": model_info["model_id"],
                        "healthy_count": 0,
                        "unhealthy_count": 0,
                        "error_message": None,
                    }
                model_results[key]["healthy_count"] += 1

    # Process unhealthy endpoints
    for endpoint in unhealthy_endpoints:
        model_param = endpoint.get("model")
        error_message = endpoint.get("error")
        if model_param and model_param in model_param_to_info:
            for model_info in model_param_to_info[model_param]:
                key = (model_info["model_id"], model_info["model_name"])
                if key not in model_results:
                    model_results[key] = {
                        "model_name": model_info["model_name"],
                        "model_id": model_info["model_id"],
                        "healthy_count": 0,
                        "unhealthy_count": 0,
                        "error_message": None,
                    }
                model_results[key]["unhealthy_count"] += 1
                # Use the first error message encountered
                if not model_results[key]["error_message"] and error_message:
                    model_results[key]["error_message"] = str(error_message)[:500]

    return model_results

