
def find_adapter_config_file(
    model_id: str,
    cache_dir: str | os.PathLike | None = None,
    force_download: bool = False,
    proxies: dict[str, str] | None = None,
    token: bool | str | None = None,
    revision: str | None = None,
    local_files_only: bool = False,
    subfolder: str = "",
    _commit_hash: str | None = None,
) -> str | None:
    r"""
    Simply checks if the model stored on the Hub or locally is an adapter model or not, return the path of the adapter
    config file if it is, None otherwise.

    Args:
        model_id (`str`):
            The identifier of the model to look for, can be either a local path or an id to the repository on the Hub.
        cache_dir (`str` or `os.PathLike`, *optional*):
            Path to a directory in which a downloaded pretrained model configuration should be cached if the standard
            cache should not be used.
        force_download (`bool`, *optional*, defaults to `False`):
            Whether or not to force to (re-)download the configuration files and override the cached versions if they
            exist.
        proxies (`dict[str, str]`, *optional*):
            A dictionary of proxy servers to use by protocol or endpoint, e.g., `{'http': 'foo.bar:3128',
            'http://hostname': 'foo.bar:4012'}.` The proxies are used on each request.
        token (`str` or *bool*, *optional*):
            The token to use as HTTP bearer authorization for remote files. If `True`, will use the token generated
            when running `hf auth login` (stored in `~/.huggingface`).
        revision (`str`, *optional*, defaults to `"main"`):
            The specific model version to use. It can be a branch name, a tag name, or a commit id, since we use a
            git-based system for storing models and other artifacts on huggingface.co, so `revision` can be any
            identifier allowed by git.

            <Tip>

            To test a pull request you made on the Hub, you can pass `revision="refs/pr/<pr_number>".

            </Tip>

        local_files_only (`bool`, *optional*, defaults to `False`):
            If `True`, will only try to load the tokenizer configuration from local files.
        subfolder (`str`, *optional*, defaults to `""`):
            In case the relevant files are located inside a subfolder of the model repo on huggingface.co, you can
            specify the folder name here.
    """
    adapter_cached_filename = None
    if model_id is None:
        return None
    elif os.path.isdir(model_id):
        list_remote_files = os.listdir(model_id)
        if ADAPTER_CONFIG_NAME in list_remote_files:
            adapter_cached_filename = os.path.join(model_id, ADAPTER_CONFIG_NAME)
    else:
        adapter_cached_filename = cached_file(
            model_id,
            ADAPTER_CONFIG_NAME,
            cache_dir=cache_dir,
            force_download=force_download,
            proxies=proxies,
            token=token,
            revision=revision,
            local_files_only=local_files_only,
            subfolder=subfolder,
            _commit_hash=_commit_hash,
            _raise_exceptions_for_gated_repo=False,
            _raise_exceptions_for_missing_entries=False,
            _raise_exceptions_for_connection_errors=False,
        )

    return adapter_cached_filename

