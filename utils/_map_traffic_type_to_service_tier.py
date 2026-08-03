from typing import Optional

def _map_traffic_type_to_service_tier(traffic_type: Optional[str]) -> Optional[str]:
    """
    Map a Gemini usageMetadata.trafficType value to a LiteLLM service_tier string.

    This allows the same `_priority` / `_flex` cost-key suffix logic used for
    OpenAI/Azure to work for Gemini and Vertex AI models.

    trafficType values seen in practice
    ------------------------------------
    ON_DEMAND          -> standard pricing  (service_tier = None)
    ON_DEMAND_PRIORITY -> priority pricing  (service_tier = "priority")
    FLEX / BATCH       -> batch/flex pricing (service_tier = "flex")
    """
    if traffic_type is None:
        return None
    service_tier = _GEMINI_TRAFFIC_TYPE_TO_SERVICE_TIER.get(str(traffic_type).upper())
    return service_tier

