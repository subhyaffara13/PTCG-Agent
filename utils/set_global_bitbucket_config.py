from typing import Any, Dict

def set_global_bitbucket_config(config: Dict[str, Any]) -> None:
    """Set global BitBucket configuration for prompt management."""
    global global_bitbucket_config
    global_bitbucket_config = config


def set_global_bitbucket_config(config: dict) -> None:
    """
    Set the global BitBucket configuration for prompt management.

    Args:
        config: Dictionary containing BitBucket configuration
                - workspace: BitBucket workspace name
                - repository: Repository name
                - access_token: BitBucket access token
                - branch: Branch to fetch prompts from (default: main)
    """
    import litellm

    litellm.global_bitbucket_config = config  # type: ignore

