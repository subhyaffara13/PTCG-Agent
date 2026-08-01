
def _summarise_usage_data(data: Dict[str, Any]) -> str:
    meta = data.get("metadata", {})
    results = data.get("results", [])

    header = (
        f"Total Spend: ${meta.get('total_spend', 0):.4f}\n"
        f"Total Requests: {meta.get('total_api_requests', 0)}\n"
        f"Successful: {meta.get('total_successful_requests', 0)} | "
        f"Failed: {meta.get('total_failed_requests', 0)}\n"
        f"Total Tokens: {meta.get('total_tokens', 0)}"
    )

    models = _accumulate_breakdown(
        results, "models", ["spend", "api_requests", "total_tokens"]
    )
    providers = _accumulate_breakdown(results, "providers", ["spend", "api_requests"])

    model_lines = _ranked_lines(
        models,
        lambda n, d: f"  - {n}: ${d['spend']:.4f} ({int(d['api_requests'])} reqs, {int(d['total_tokens'])} tokens)",
        TOP_N_MODELS,
    )
    provider_lines = _ranked_lines(
        providers,
        lambda n, d: f"  - {n}: ${d['spend']:.4f} ({int(d['api_requests'])} reqs)",
        TOP_N_PROVIDERS,
    )

    sections = [header, ""]
    sections += ["Top Models by Spend:"] + (model_lines or ["  (no data)"]) + [""]
    sections += ["Top Providers by Spend:"] + (provider_lines or ["  (no data)"])
    return "\n".join(sections)

