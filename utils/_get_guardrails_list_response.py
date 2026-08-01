
def _get_guardrails_list_response(
    guardrails_config: List[Dict],
) -> ListGuardrailsResponse:
    """
    Helper function to get the guardrails list response
    """
    from litellm.litellm_core_utils.litellm_logging import _get_masked_values

    guardrail_configs: List[GuardrailInfoResponse] = []
    for guardrail in guardrails_config:
        litellm_params = guardrail.get("litellm_params") or {}
        masked_params = _get_masked_values(
            litellm_params,
            unmasked_length=4,
            number_of_asterisks=4,
        )
        guardrail_configs.append(
            GuardrailInfoResponse(
                guardrail_name=guardrail.get("guardrail_name"),
                litellm_params=masked_params,
                guardrail_info=guardrail.get("guardrail_info"),
            )
        )
    return ListGuardrailsResponse(guardrails=guardrail_configs)

