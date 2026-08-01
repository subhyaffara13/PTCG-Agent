
def cost_per_web_search_request(usage: "Usage", model_info: "ModelInfo") -> float:
    """
    Calculates the cost of web search (grounding with Google Search).

    Billing mode is determined by ``web_search_billing_unit`` in model_info:
    - ``"per_query"``: charged per individual search query (Gemini 3.x).
    - ``"per_prompt"`` (default): charged per grounded prompt (Gemini 2.x),
      regardless of how many queries were executed internally.

    Reads the per-request cost from ``search_context_cost_per_query`` in
    ``model_info`` when available, falling back to $0.035 for models not
    yet updated in the pricing JSON.
    """
    from litellm.types.utils import PromptTokensDetailsWrapper

    _DEFAULT_COST = 35e-3
    search_costs = model_info.get("search_context_cost_per_query") or {}
    _cost = search_costs.get("search_context_size_medium", _DEFAULT_COST)

    number_of_web_search_requests = 0
    if (
        usage is not None
        and usage.prompt_tokens_details is not None
        and isinstance(usage.prompt_tokens_details, PromptTokensDetailsWrapper)
        and hasattr(usage.prompt_tokens_details, "web_search_requests")
        and usage.prompt_tokens_details.web_search_requests is not None
    ):
        number_of_web_search_requests = usage.prompt_tokens_details.web_search_requests

    # per_prompt billing: clamp to 1 (flat fee per grounded API call)
    billing_mode = model_info.get("web_search_billing_unit", "per_prompt")
    if number_of_web_search_requests > 0 and billing_mode == "per_prompt":
        number_of_web_search_requests = 1

    return _cost * number_of_web_search_requests


def cost_per_web_search_request(usage: "Usage", model_info: "ModelInfo") -> float:
    """
    Calculate the cost of web search requests for X.AI models.

    X.AI Live Search costs $25 per 1,000 sources used.
    Each source costs $0.025.

    The number of sources is stored in prompt_tokens_details.web_search_requests
    by the transformation layer to be compatible with the existing detection system.
    """
    # Cost per source used: $25 per 1,000 sources = $0.025 per source
    cost_per_source = 25.0 / 1000.0  # $0.025

    num_sources_used = 0

    if (
        hasattr(usage, "prompt_tokens_details")
        and usage.prompt_tokens_details is not None
        and hasattr(usage.prompt_tokens_details, "web_search_requests")
        and usage.prompt_tokens_details.web_search_requests is not None
    ):
        num_sources_used = int(usage.prompt_tokens_details.web_search_requests)

    # Fallback: try to get from num_sources_used if set directly
    elif hasattr(usage, "num_sources_used") and usage.num_sources_used is not None:
        num_sources_used = int(usage.num_sources_used)

    total_cost = cost_per_source * num_sources_used

    return total_cost


def cost_per_web_search_request(usage: "Usage", model_info: "ModelInfo") -> float:
    """
    Calculate the cost of a web search request for Vertex AI Gemini.

    Billing differs by ``web_search_billing_unit`` in ``model_info``:
    - ``"per_query"``: charged per individual search query (Gemini 3.x).
    - ``"per_prompt"`` (default): charged per grounded prompt (Gemini 2.x).

    Delegates to the shared Gemini cost calculator.
    """
    from litellm.llms.gemini.cost_calculator import (
        cost_per_web_search_request as _gemini_cost,
    )

    return _gemini_cost(usage=usage, model_info=model_info)

