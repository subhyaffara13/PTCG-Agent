
def dump_environment_info() -> dict[str, Any]:
    """Dump information about the machine to help debugging issues.

    Similar helper exist in:
    - `datasets` (https://github.com/huggingface/datasets/blob/main/src/datasets/commands/env.py)
    - `diffusers` (https://github.com/huggingface/diffusers/blob/main/src/diffusers/commands/env.py)
    - `transformers` (https://github.com/huggingface/transformers/blob/main/src/transformers/commands/env.py)
    """
    from huggingface_hub import get_token, whoami
    from huggingface_hub.utils import is_agent, list_credential_helpers

    token = get_token()

    # Generic machine info
    info: dict[str, Any] = {
        "huggingface_hub version": get_hf_hub_version(),
        "Platform": platform.platform(),
        "Python version": get_python_version(),
    }

    # Interpreter info
    try:
        shell_class = get_ipython().__class__  # type: ignore # noqa: F821
        info["Running in iPython ?"] = "Yes"
        info["iPython shell"] = shell_class.__name__
    except NameError:
        info["Running in iPython ?"] = "No"
    info["Running in notebook ?"] = "Yes" if is_notebook() else "No"
    info["Running in Google Colab ?"] = "Yes" if is_google_colab() else "No"
    info["Running in Google Colab Enterprise ?"] = "Yes" if is_colab_enterprise() else "No"
    # Login info
    info["Token path ?"] = constants.HF_TOKEN_PATH
    info["Has saved token ?"] = token is not None
    if token is not None:
        try:
            info["Who am I ?"] = whoami()["name"]
        except Exception:
            pass

    try:
        info["Configured git credential helpers"] = ", ".join(list_credential_helpers())
    except Exception:
        pass

    info["Run by AI agent ?"] = "Yes" if is_agent() else "No"

    # How huggingface_hub has been installed?
    info["Installation method"] = installation_method()

    # Installed dependencies
    info["httpx"] = get_httpx_version()
    info["hf_xet"] = get_xet_version()
    info["gradio"] = get_gradio_version()
    info["tensorboard"] = get_tensorboard_version()

    # Environment variables
    info["ENDPOINT"] = constants.ENDPOINT
    info["HF_HUB_CACHE"] = constants.HF_HUB_CACHE
    info["HF_ASSETS_CACHE"] = constants.HF_ASSETS_CACHE
    info["HF_TOKEN_PATH"] = constants.HF_TOKEN_PATH
    info["HF_STORED_TOKENS_PATH"] = constants.HF_STORED_TOKENS_PATH
    info["HF_HUB_OFFLINE"] = constants.HF_HUB_OFFLINE
    info["HF_HUB_DISABLE_TELEMETRY"] = constants.HF_HUB_DISABLE_TELEMETRY
    info["HF_HUB_DISABLE_PROGRESS_BARS"] = constants.HF_HUB_DISABLE_PROGRESS_BARS
    info["HF_HUB_DISABLE_SYMLINKS"] = constants.HF_HUB_DISABLE_SYMLINKS
    info["HF_HUB_DISABLE_SYMLINKS_WARNING"] = constants.HF_HUB_DISABLE_SYMLINKS_WARNING
    info["HF_HUB_DISABLE_EXPERIMENTAL_WARNING"] = constants.HF_HUB_DISABLE_EXPERIMENTAL_WARNING
    info["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = constants.HF_HUB_DISABLE_IMPLICIT_TOKEN
    info["HF_HUB_DISABLE_XET"] = constants.HF_HUB_DISABLE_XET
    info["HF_HUB_ETAG_TIMEOUT"] = constants.HF_HUB_ETAG_TIMEOUT
    info["HF_HUB_DOWNLOAD_TIMEOUT"] = constants.HF_HUB_DOWNLOAD_TIMEOUT
    info["HF_XET_HIGH_PERFORMANCE"] = constants.HF_XET_HIGH_PERFORMANCE

    print("\nCopy-and-paste the text below in your GitHub issue.\n")
    print("\n".join([f"- {prop}: {val}" for prop, val in info.items()]) + "\n")
    return info

