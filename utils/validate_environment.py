import os
import sys
from typing import List, Optional

def validate_environment(
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
) -> dict:
    """
    Checks if the environment variables are valid for the given model.

    Args:
        model (Optional[str]): The name of the model. Defaults to None.
        api_key (Optional[str]): If the user passed in an api key, of their own.

    Returns:
        dict: A dictionary containing the following keys:
            - keys_in_environment (bool): True if all the required keys are present in the environment, False otherwise.
            - missing_keys (List[str]): A list of missing keys in the environment.
    """
    keys_in_environment = False
    missing_keys: List[str] = []

    if model is None:
        return {
            "keys_in_environment": keys_in_environment,
            "missing_keys": missing_keys,
        }
    ## EXTRACT LLM PROVIDER - if model name provided
    try:
        get_llm_provider = getattr(sys.modules[__name__], "get_llm_provider")
        _, custom_llm_provider, _, _ = get_llm_provider(model=model)
    except Exception:
        custom_llm_provider = None

    if custom_llm_provider:
        if custom_llm_provider == "openai":
            if "OPENAI_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("OPENAI_API_KEY")
        elif custom_llm_provider == "azure":
            if (
                "AZURE_API_BASE" in os.environ
                and "AZURE_API_VERSION" in os.environ
                and "AZURE_API_KEY" in os.environ
            ):
                keys_in_environment = True
            else:
                missing_keys.extend(
                    ["AZURE_API_BASE", "AZURE_API_VERSION", "AZURE_API_KEY"]
                )
        elif custom_llm_provider == "anthropic":
            if (
                "ANTHROPIC_API_KEY" in os.environ
                or "ANTHROPIC_AUTH_TOKEN" in os.environ
            ):
                keys_in_environment = True
            else:
                missing_keys.append("ANTHROPIC_API_KEY")
        elif custom_llm_provider == "cohere":
            if "COHERE_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("COHERE_API_KEY")
        elif custom_llm_provider == "replicate":
            if "REPLICATE_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("REPLICATE_API_KEY")
        elif custom_llm_provider == "openrouter":
            if "OPENROUTER_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("OPENROUTER_API_KEY")
        elif custom_llm_provider == "vercel_ai_gateway":
            if "VERCEL_AI_GATEWAY_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("VERCEL_AI_GATEWAY_API_KEY")
        elif custom_llm_provider == "datarobot":
            if "DATAROBOT_API_TOKEN" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("DATAROBOT_API_TOKEN")
        elif custom_llm_provider == "vertex_ai":
            if "VERTEXAI_PROJECT" in os.environ and "VERTEXAI_LOCATION" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.extend(["VERTEXAI_PROJECT", "VERTEXAI_LOCATION"])
        elif custom_llm_provider == "huggingface":
            if "HUGGINGFACE_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("HUGGINGFACE_API_KEY")
        elif custom_llm_provider == "ai21":
            if "AI21_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("AI21_API_KEY")
        elif custom_llm_provider == "together_ai":
            if "TOGETHERAI_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("TOGETHERAI_API_KEY")
        elif custom_llm_provider == "aleph_alpha":
            if "ALEPH_ALPHA_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("ALEPH_ALPHA_API_KEY")
        elif custom_llm_provider == "baseten":
            if "BASETEN_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("BASETEN_API_KEY")
        elif custom_llm_provider == "nlp_cloud":
            if "NLP_CLOUD_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("NLP_CLOUD_API_KEY")
        elif custom_llm_provider == "bedrock" or custom_llm_provider == "sagemaker":
            if (
                "AWS_ACCESS_KEY_ID" in os.environ
                and "AWS_SECRET_ACCESS_KEY" in os.environ
            ) or (
                # IAM role, profile, or web identity auth don't require access keys
                "AWS_ROLE_ARN" in os.environ
                or "AWS_PROFILE" in os.environ
                or "AWS_WEB_IDENTITY_TOKEN_FILE" in os.environ
                or "AWS_CONTAINER_CREDENTIALS_RELATIVE_URI"
                in os.environ  # ECS task role
                or "AWS_CONTAINER_CREDENTIALS_FULL_URI"
                in os.environ  # ECS/Fargate full URI credential delivery
            ):
                keys_in_environment = True
            else:
                missing_keys.append("AWS_ACCESS_KEY_ID")
                missing_keys.append("AWS_SECRET_ACCESS_KEY")
        elif custom_llm_provider in ["ollama", "ollama_chat"]:
            if "OLLAMA_API_BASE" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("OLLAMA_API_BASE")
        elif custom_llm_provider == "anyscale":
            if "ANYSCALE_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("ANYSCALE_API_KEY")
        elif custom_llm_provider == "deepinfra":
            if "DEEPINFRA_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("DEEPINFRA_API_KEY")
        elif custom_llm_provider == "featherless_ai":
            if "FEATHERLESS_AI_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("FEATHERLESS_AI_API_KEY")
        elif custom_llm_provider == "gemini":
            if ("GOOGLE_API_KEY" in os.environ) or ("GEMINI_API_KEY" in os.environ):
                keys_in_environment = True
            else:
                missing_keys.append("GOOGLE_API_KEY")
                missing_keys.append("GEMINI_API_KEY")
        elif custom_llm_provider == "groq":
            if "GROQ_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("GROQ_API_KEY")
        elif custom_llm_provider == "nvidia_nim":
            if "NVIDIA_NIM_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("NVIDIA_NIM_API_KEY")
        elif custom_llm_provider == "cerebras":
            if "CEREBRAS_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("CEREBRAS_API_KEY")
        elif custom_llm_provider == "baseten":
            if "BASETEN_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("BASETEN_API_KEY")
        elif custom_llm_provider == "xai":
            if "XAI_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("XAI_API_KEY")
        elif custom_llm_provider == "ai21_chat":
            if "AI21_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("AI21_API_KEY")
        elif custom_llm_provider == "volcengine":
            if "VOLCENGINE_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("VOLCENGINE_API_KEY")
        elif (
            custom_llm_provider == "codestral"
            or custom_llm_provider == "text-completion-codestral"
        ):
            if "CODESTRAL_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("CODESTRAL_API_KEY")
        elif (
            custom_llm_provider == "inception"
            or custom_llm_provider == "text-completion-inception"
        ):
            if "INCEPTION_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("INCEPTION_API_KEY")
        elif custom_llm_provider == "deepseek":
            if "DEEPSEEK_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("DEEPSEEK_API_KEY")
        elif custom_llm_provider == "mistral":
            if "MISTRAL_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("MISTRAL_API_KEY")
        elif custom_llm_provider == "palm":
            if "PALM_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("PALM_API_KEY")
        elif custom_llm_provider == "perplexity":
            if "PERPLEXITYAI_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("PERPLEXITYAI_API_KEY")
        elif custom_llm_provider == "voyage":
            if "VOYAGE_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("VOYAGE_API_KEY")
        elif custom_llm_provider == "infinity":
            if "INFINITY_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("INFINITY_API_KEY")
        elif custom_llm_provider == "fireworks_ai":
            if (
                "FIREWORKS_AI_API_KEY" in os.environ
                or "FIREWORKS_API_KEY" in os.environ
                or "FIREWORKSAI_API_KEY" in os.environ
                or "FIREWORKS_AI_TOKEN" in os.environ
            ):
                keys_in_environment = True
            else:
                missing_keys.append("FIREWORKS_AI_API_KEY")
        elif custom_llm_provider == "cloudflare":
            if "CLOUDFLARE_API_KEY" in os.environ and (
                "CLOUDFLARE_ACCOUNT_ID" in os.environ
                or "CLOUDFLARE_API_BASE" in os.environ
            ):
                keys_in_environment = True
            else:
                missing_keys.append("CLOUDFLARE_API_KEY")
                missing_keys.append("CLOUDFLARE_API_BASE")
        elif custom_llm_provider == "novita":
            if "NOVITA_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("NOVITA_API_KEY")
        elif custom_llm_provider == "nebius":
            if "NEBIUS_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("NEBIUS_API_KEY")
        elif custom_llm_provider == "wandb":
            if "WANDB_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("WANDB_API_KEY")
        elif custom_llm_provider == "dashscope":
            if "DASHSCOPE_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("DASHSCOPE_API_KEY")
        elif custom_llm_provider == "modelscope":
            if "MODELSCOPE_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("MODELSCOPE_API_KEY")
        elif custom_llm_provider == "moonshot":
            if "MOONSHOT_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("MOONSHOT_API_KEY")
    else:
        ## openai - chatcompletion + text completion
        if (
            model in litellm.open_ai_chat_completion_models
            or model in litellm.open_ai_text_completion_models
            or model in litellm.open_ai_embedding_models
            or model in litellm.openai_image_generation_models
            or model.startswith("gpt-image")
        ):
            if "OPENAI_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("OPENAI_API_KEY")
        ## anthropic
        elif model in litellm.anthropic_models:
            if (
                "ANTHROPIC_API_KEY" in os.environ
                or "ANTHROPIC_AUTH_TOKEN" in os.environ
            ):
                keys_in_environment = True
            else:
                missing_keys.append("ANTHROPIC_API_KEY")
        ## cohere
        elif model in litellm.cohere_models:
            if "COHERE_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("COHERE_API_KEY")
        ## replicate
        elif model in litellm.replicate_models:
            if "REPLICATE_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("REPLICATE_API_KEY")
        ## openrouter
        elif model in litellm.openrouter_models:
            if "OPENROUTER_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("OPENROUTER_API_KEY")
        ## vercel_ai_gateway
        elif model in litellm.vercel_ai_gateway_models:
            if "VERCEL_AI_GATEWAY_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("VERCEL_AI_GATEWAY_API_KEY")
        ## datarobot
        elif model in litellm.datarobot_models:
            if "DATAROBOT_API_TOKEN" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("DATAROBOT_API_TOKEN")
        ## vertex - text + chat models
        elif (
            model in litellm.vertex_chat_models
            or model in litellm.vertex_text_models
            or model in litellm.models_by_provider["vertex_ai"]
        ):
            if "VERTEXAI_PROJECT" in os.environ and "VERTEXAI_LOCATION" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.extend(["VERTEXAI_PROJECT", "VERTEXAI_LOCATION"])
        ## huggingface
        elif model in litellm.huggingface_models:
            if "HUGGINGFACE_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("HUGGINGFACE_API_KEY")
        ## ai21
        elif model in litellm.ai21_models:
            if "AI21_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("AI21_API_KEY")
        ## together_ai
        elif model in litellm.together_ai_models:
            if "TOGETHERAI_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("TOGETHERAI_API_KEY")
        ## aleph_alpha
        elif model in litellm.aleph_alpha_models:
            if "ALEPH_ALPHA_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("ALEPH_ALPHA_API_KEY")
        ## baseten
        elif model in litellm.baseten_models:
            if "BASETEN_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("BASETEN_API_KEY")
        ## nlp_cloud
        elif model in litellm.nlp_cloud_models:
            if "NLP_CLOUD_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("NLP_CLOUD_API_KEY")
        elif model in litellm.novita_models:
            if "NOVITA_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("NOVITA_API_KEY")
        elif model in litellm.nebius_models:
            if "NEBIUS_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("NEBIUS_API_KEY")
        elif model in litellm.wandb_models:
            if "WANDB_API_KEY" in os.environ:
                keys_in_environment = True
            else:
                missing_keys.append("WANDB_API_KEY")

    def filter_missing_keys(keys: List[str], exclude_pattern: str) -> List[str]:
        """Filter out keys that contain the exclude_pattern (case insensitive)."""
        return [key for key in keys if exclude_pattern not in key.lower()]

    if api_key is not None:
        missing_keys = filter_missing_keys(missing_keys, "api_key")

    if api_base is not None:
        missing_keys = filter_missing_keys(missing_keys, "api_base")

    if api_version is not None:
        missing_keys = filter_missing_keys(missing_keys, "api_version")

    if len(missing_keys) == 0:  # no missing keys
        keys_in_environment = True

    return {"keys_in_environment": keys_in_environment, "missing_keys": missing_keys}


def validate_environment():
    if "AWS_REGION_NAME" not in os.environ:
        raise ValueError("Missing required environment variable - AWS_REGION_NAME")


def validate_environment():
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise ValueError(
            "Missing required environment variable - GOOGLE_APPLICATION_CREDENTIALS"
        )
    if "GOOGLE_KMS_RESOURCE_NAME" not in os.environ:
        raise ValueError(
            "Missing required environment variable - GOOGLE_KMS_RESOURCE_NAME"
        )


def validate_environment(
    headers: dict,
    model: str,
    messages: List[AllMessageValues],
    optional_params: dict,
    api_key: Optional[str] = None,
) -> dict:
    """
    Return headers to use for cohere chat completion request

    Cohere API Ref: https://docs.cohere.com/reference/chat
    Expected headers:
    {
        "Request-Source": "unspecified:litellm",
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer $CO_API_KEY"
    }
    """
    headers.update(
        {
            "Request-Source": "unspecified:litellm",
            "accept": "application/json",
            "content-type": "application/json",
        }
    )
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def validate_environment(api_key):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def validate_environment(model: str):
    global llm
    try:
        from vllm import LLM, SamplingParams  # type: ignore

        if llm is None:
            llm = LLM(model=model)
        return llm, SamplingParams
    except Exception as e:
        raise VLLMError(status_code=0, message=str(e))


def validate_environment(api_key, headers: dict):
    # Create a lowercase key lookup to avoid duplicate headers with different cases
    # This is important when headers come from AWS signed requests (which use Title-Case)
    existing_keys_lower = {k.lower(): k for k in headers.keys()}

    # Only add headers if they don't already exist (case-insensitive check)
    if "request-source" not in existing_keys_lower:
        headers["Request-Source"] = "unspecified:litellm"
    if "accept" not in existing_keys_lower:
        headers["accept"] = "application/json"
    if "content-type" not in existing_keys_lower:
        headers["content-type"] = "application/json"
    if api_key and "authorization" not in existing_keys_lower:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def validate_environment(environment: str):
    if environment not in [env.value for env in Environment]:
        valid_values = ", ".join(f'"{env.value}"' for env in Environment)
        raise ValueError(
            f"Invalid environment: {environment}. Please use one of the following instead: {valid_values}"
        )

