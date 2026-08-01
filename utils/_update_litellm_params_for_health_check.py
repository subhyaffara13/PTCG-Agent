
def _update_litellm_params_for_health_check(
    model_info: dict, litellm_params: dict
) -> dict:
    """
    Update the litellm params for health check.

    - gets a short `messages` param for health check
    - adds a bounded `max_tokens` when the deployment is a chat-style mode
      (`chat`, `completion`, `responses`) or the operator explicitly opts in
      via `model_info.health_check_supports_max_tokens`. Non-chat endpoints
      (image, embedding, audio_*, rerank, video, ocr, search, moderation, ...)
      reject unknown fields with 400 "Unknown parameter: 'max_tokens'".
    - updates the `model` param with the `health_check_model` if it exists Doc: https://docs.litellm.ai/docs/proxy/health#wildcard-routes
    - updates the `voice` param with the `health_check_voice` for `audio_speech` mode if it exists Doc: https://docs.litellm.ai/docs/proxy/health#text-to-speech-models
    - for Bedrock models with region routing (bedrock/region/model), strips the litellm routing prefix but preserves the model ID, and pins `custom_llm_provider` to `bedrock` (only when the deployment hasn't already set one, so an explicit `bedrock_converse` survives) so the bare model id still resolves to the provider (e.g. cross-region ids like `us.cohere.embed-v4:0`)
    """
    mode = _resolve_health_check_mode(
        model_info, litellm_params  # any-ok: untyped router config dict
    )
    litellm_params["messages"] = _get_random_llm_message()
    if _should_inject_health_check_max_tokens(
        model_info, mode  # any-ok: untyped router config dict
    ):
        _resolved_max_tokens = _resolve_health_check_max_tokens(
            model_info, litellm_params
        )
        if _resolved_max_tokens is not None:
            litellm_params["max_tokens"] = _resolved_max_tokens

    # Per-model reasoning effort for health checks only (e.g. reasoning_effort=none).
    if mode in _HEALTH_CHECK_MODES_SUPPORTING_REASONING_EFFORT:
        _hc_reasoning_effort = model_info.get("health_check_reasoning_effort", None)
        if _hc_reasoning_effort is not None:
            litellm_params["reasoning_effort"] = _hc_reasoning_effort

    _health_check_model = model_info.get("health_check_model", None)
    if _health_check_model is not None:
        litellm_params["model"] = _health_check_model
    if mode == "audio_speech":
        litellm_params["voice"] = model_info.get("health_check_voice", "alloy")

    # Handle Bedrock region routing format: bedrock/region/model
    # This is needed because health checks bypass get_llm_provider() for the model param
    # Issue #15807: Without this, health checks send "region/model" as the model ID to AWS
    # which causes: "bedrock-runtime.../model/us-west-2/mistral.../invoke" (region in model ID)
    #
    # However, we must preserve cross-region inference profile prefixes like "us.", "eu.", etc.
    # Issue: Stripping these breaks AWS requirement for inference profile IDs
    #
    # Must also preserve route prefixes (converse/, invoke/) and handlers (llama/, deepseek_r1/, etc.)
    if litellm_params["model"].startswith("bedrock/"):
        from litellm.llms.bedrock.common_utils import BedrockModelInfo

        model = litellm_params["model"]
        # Strip only the bedrock/ prefix (preserve routes like converse/, invoke/)
        if model.startswith("bedrock/"):
            model = model[8:]  # len("bedrock/") = 8

        # Now check for region routing and strip it if present
        # Need to handle formats like:
        # - "us-west-2/model" → "model"
        # - "converse/us-west-2/model" → "converse/model"
        # - "llama/arn:..." → "llama/arn:..." (preserve handler)
        #
        # Strategy: Check each path segment, remove regions, preserve everything else
        parts = model.split("/")
        filtered_parts = []

        for part in parts:
            # Skip AWS regions, keep everything else
            if part not in BedrockModelInfo.all_global_regions:
                filtered_parts.append(part)

        model = "/".join(filtered_parts)
        litellm_params["model"] = model
        if not litellm_params.get("custom_llm_provider"):  # any-ok: untyped router dict
            litellm_params["custom_llm_provider"] = (  # any-ok: untyped router dict
                "bedrock"
            )

    return litellm_params

