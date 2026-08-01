
def set_global_gitlab_config(config: Dict[str, Any]) -> None:
    """Set global BitBucket configuration for prompt management."""
    global global_gitlab_config
    global_gitlab_config = config


def set_global_gitlab_config(config: dict) -> None:
    """
    Set the global gitlab configuration for prompt management.

    Args:
        config: Dictionary containing gitlab configuration
                - workspace: gitlab workspace name
                - repository: Repository name
                - access_token: gitlab access token
                - branch: Branch to fetch prompts from (default: main)
    """
    import litellm

    litellm.global_gitlab_config = config  # type: ignore

