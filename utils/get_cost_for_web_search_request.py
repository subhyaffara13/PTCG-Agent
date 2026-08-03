from typing import Optional

def get_cost_for_web_search_request(
    custom_llm_provider: str, usage: "Usage", model_info: "ModelInfo"
) -> Optional[float]:
    """
    Get the cost for a web search request for a given model.

    Args:
        custom_llm_provider: The custom LLM provider.
        usage: The usage object.
        model_info: The model info.
    """
    if custom_llm_provider == "gemini":
        from .gemini.cost_calculator import cost_per_web_search_request

        return cost_per_web_search_request(usage=usage, model_info=model_info)
    elif custom_llm_provider == "anthropic":
        from .anthropic.cost_calculation import get_cost_for_anthropic_web_search

        return get_cost_for_anthropic_web_search(model_info=model_info, usage=usage)
    elif custom_llm_provider.startswith("vertex_ai"):
        # Anthropic Claude models on Vertex AI populate server_tool_use.web_search_requests
        # (same as the direct Anthropic API), not prompt_tokens_details.web_search_requests
        # (which is the Gemini field). Route claude-* models to the Anthropic calculator.
        model_key: str = model_info.get("key", "") if model_info else ""
        if "claude" in model_key.lower():
            from .anthropic.cost_calculation import get_cost_for_anthropic_web_search

            verbose_logger.debug(
                "vertex_ai/claude model detected — routing web search cost to Anthropic calculator"
            )
            return get_cost_for_anthropic_web_search(model_info=model_info, usage=usage)

        from .vertex_ai.gemini.cost_calculator import (
            cost_per_web_search_request as cost_per_web_search_request_vertex_ai,
        )

        return cost_per_web_search_request_vertex_ai(usage=usage, model_info=model_info)
    elif custom_llm_provider == "perplexity":
        # Perplexity handles search costs internally in its own cost calculator
        # Return 0.0 to indicate costs are already accounted for
        return 0.0
    elif custom_llm_provider == "xai":
        from .xai.cost_calculator import cost_per_web_search_request

        return cost_per_web_search_request(usage=usage, model_info=model_info)
    else:
        return None

