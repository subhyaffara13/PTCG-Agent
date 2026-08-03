import os

def prompt_initializer(
    litellm_params: "PromptLiteLLMParams", prompt_spec: "PromptSpec"
) -> "CustomPromptManagement":
    """
    Initialize a prompt from Arize Phoenix.
    """
    api_key = getattr(litellm_params, "api_key", None) or os.environ.get(
        "PHOENIX_API_KEY"
    )
    api_base = getattr(litellm_params, "api_base", None)
    prompt_id = getattr(litellm_params, "prompt_id", None)

    if not api_key or not api_base:
        raise ValueError(
            "api_key and api_base are required for Arize Phoenix prompt integration"
        )

    try:
        arize_prompt_manager = ArizePhoenixPromptManager(
            **{
                "api_key": api_key,
                "api_base": api_base,
                "prompt_id": prompt_id,
                **litellm_params.model_dump(
                    exclude={"api_key", "api_base", "prompt_id"}
                ),
            },
        )

        return arize_prompt_manager
    except Exception as e:
        raise e


def prompt_initializer(
    litellm_params: "PromptLiteLLMParams", prompt_spec: "PromptSpec"
) -> "CustomPromptManagement":
    """
    Initialize a prompt from a BitBucket repository.
    """
    bitbucket_config = getattr(litellm_params, "bitbucket_config", None)
    prompt_id = getattr(litellm_params, "prompt_id", None)

    if not bitbucket_config:
        raise ValueError(
            "bitbucket_config is required for BitBucket prompt integration"
        )

    try:
        bitbucket_prompt_manager = BitBucketPromptManager(
            bitbucket_config=bitbucket_config,
            prompt_id=prompt_id,
        )

        return bitbucket_prompt_manager
    except Exception as e:
        raise e


def prompt_initializer(
    litellm_params: "PromptLiteLLMParams", prompt_spec: "PromptSpec"
) -> "CustomPromptManagement":
    """
    Initialize a prompt from a .prompt file.
    """
    prompt_directory = getattr(litellm_params, "prompt_directory", None)
    prompt_data = getattr(litellm_params, "prompt_data", None)
    prompt_id = getattr(litellm_params, "prompt_id", None)
    if prompt_directory:
        raise ValueError(
            "Cannot set prompt_directory when working with prompt_initializer. Needs to be a specific dotprompt file"
        )

    prompt_file = getattr(litellm_params, "prompt_file", None)

    # Handle dotprompt_content from database
    dotprompt_content = getattr(litellm_params, "dotprompt_content", None)
    if dotprompt_content and not prompt_data and not prompt_file:
        prompt_data = _get_prompt_data_from_dotprompt_content(dotprompt_content)

    try:
        dot_prompt_manager = DotpromptManager(
            prompt_directory=prompt_directory,
            prompt_data=prompt_data,
            prompt_file=prompt_file,
            prompt_id=prompt_id,
        )

        return dot_prompt_manager
    except Exception as e:
        raise e


def prompt_initializer(
    litellm_params: "PromptLiteLLMParams", prompt_spec: "PromptSpec"
) -> "CustomPromptManagement":
    """
    Initialize a prompt from a generic prompt management API.
    """
    prompt_id = getattr(litellm_params, "prompt_id", None)

    api_base = litellm_params.api_base
    api_key = litellm_params.api_key
    if not api_base:
        raise ValueError("api_base is required in generic_prompt_config")

    provider_specific_query_params = litellm_params.provider_specific_query_params

    try:
        generic_prompt_manager = GenericPromptManager(
            api_base=api_base,
            api_key=api_key,
            prompt_id=prompt_id,
            additional_provider_specific_query_params=provider_specific_query_params,
            **litellm_params.model_dump(
                exclude_none=True,
                exclude={
                    "prompt_id",
                    "api_key",
                    "provider_specific_query_params",
                    "api_base",
                },
            ),
        )

        return generic_prompt_manager
    except Exception as e:
        raise e


def prompt_initializer(
    litellm_params: "PromptLiteLLMParams", prompt_spec: "PromptSpec"
) -> "CustomPromptManagement":
    """
    Initialize a prompt from a Gitlab repository.
    """
    gitlab_config = getattr(litellm_params, "gitlab_config", None)
    prompt_id = getattr(litellm_params, "prompt_id", None)

    if not gitlab_config:
        raise ValueError("gitlab_config is required for gitlab prompt integration")

    try:
        gitlab_prompt_manager = GitLabPromptManager(
            gitlab_config=gitlab_config,
            prompt_id=prompt_id,
        )

        return gitlab_prompt_manager
    except Exception as e:
        raise e

