
def _gitlab_prompt_initializer(
    litellm_params: PromptLiteLLMParams,
    prompt: PromptSpec,
) -> CustomPromptManagement:
    """
    Build a GitLab-backed prompt manager for this prompt.
    Expected fields on litellm_params:
      - prompt_integration="gitlab"  (handled by the caller)
      - gitlab_config: Dict[str, Any] (project/access_token/branch/prompts_path/etc.)
      - git_ref (optional): per-prompt tag/branch/SHA override
    """
    # You can store arbitrary integration-specific config on PromptLiteLLMParams.
    # If your dataclass doesn't have these attributes, add them or put inside
    # `litellm_params.extra` and pull them from there.
    gitlab_config: Dict[str, Any] = getattr(litellm_params, "gitlab_config", None) or {}
    git_ref: Optional[str] = getattr(litellm_params, "git_ref", None)

    if not gitlab_config:
        raise ValueError("gitlab_config is required for gitlab prompt integration")

    # prompt.prompt_id can map to a file path under prompts_path (e.g. "chat/greet/hi")
    return GitLabPromptManager(
        gitlab_config=gitlab_config,
        prompt_id=prompt.prompt_id,
        ref=git_ref,
    )

