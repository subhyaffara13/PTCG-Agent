
def initialize_presidio(litellm_params: LitellmParams, guardrail: Guardrail):
    from litellm.proxy.guardrails.guardrail_hooks.presidio import (
        _OPTIONAL_PresidioPIIMasking,
    )

    filter_scope = getattr(litellm_params, "presidio_filter_scope", None) or "both"
    run_input = filter_scope in ("input", "both")
    run_output = filter_scope in ("output", "both")

    def _make_presidio_callback(**overrides):
        params = dict(
            guardrail_name=guardrail.get("guardrail_name", ""),
            event_hook=litellm_params.mode,
            output_parse_pii=litellm_params.output_parse_pii,
            presidio_ad_hoc_recognizers=litellm_params.presidio_ad_hoc_recognizers,
            mock_redacted_text=litellm_params.mock_redacted_text,
            default_on=litellm_params.default_on,
            pii_entities_config=litellm_params.pii_entities_config,
            presidio_score_thresholds=litellm_params.presidio_score_thresholds,
            presidio_analyzer_api_base=litellm_params.presidio_analyzer_api_base,
            presidio_anonymizer_api_base=litellm_params.presidio_anonymizer_api_base,
            presidio_language=litellm_params.presidio_language,
            presidio_entities_deny_list=litellm_params.presidio_entities_deny_list,
            apply_to_output=False,
        )
        params.update(overrides)
        callback = _OPTIONAL_PresidioPIIMasking(**params)
        litellm.logging_callback_manager.add_litellm_callback(callback)
        return callback

    primary_callback = None

    if run_input:
        primary_callback = _make_presidio_callback()

        if litellm_params.output_parse_pii:
            _make_presidio_callback(
                output_parse_pii=True,
                event_hook=GuardrailEventHooks.post_call.value,
            )

    if run_output:
        output_callback = _make_presidio_callback(
            apply_to_output=True,
            event_hook=GuardrailEventHooks.post_call.value,
            output_parse_pii=False,
        )
        if primary_callback is None:
            primary_callback = output_callback

    return primary_callback

