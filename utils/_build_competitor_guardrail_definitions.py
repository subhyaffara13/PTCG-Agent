
def _build_competitor_guardrail_definitions(
    definitions: list,
    competitors: list,
    brand_name: str,
    variations_map: Optional[dict] = None,
) -> list:
    """Build enriched guardrailDefinitions with competitor names and variations populated."""
    variations_map = variations_map or {}
    enriched = copy.deepcopy(definitions)
    all_names = _build_all_names_per_competitor(competitors, variations_map)

    output_blocked = _build_name_blocked_words(competitors, all_names)
    recommendation_blocked = _build_recommendation_blocked_words(competitors, all_names)
    comparison_blocked = _build_comparison_blocked_words(
        competitors, all_names, brand_name
    )

    blocked_words_map = {
        "competitor-output-blocker": output_blocked,
        "competitor-input-blocker": output_blocked,
        "competitor-name-blocker": output_blocked,
        "competitor-name-input-blocker": output_blocked,
        "competitor-name-output-blocker": output_blocked,
        "competitor-recommendation-filter": recommendation_blocked,
        "competitor-recommendation-input-filter": recommendation_blocked,
        "competitor-recommendation-output-filter": recommendation_blocked,
        "competitor-comparison-filter": comparison_blocked,
        "competitor-comparison-input-filter": comparison_blocked,
        "competitor-comparison-output-filter": comparison_blocked,
    }

    for defn in enriched:
        guardrail_name = defn.get("guardrail_name", "")
        if guardrail_name in blocked_words_map:
            defn["litellm_params"]["blocked_words"] = blocked_words_map[guardrail_name]

    return enriched

