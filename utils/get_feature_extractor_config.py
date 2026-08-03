import os

def get_feature_extractor_config(
    pretrained_model_name_or_path: str | os.PathLike,
    cache_dir: str | os.PathLike | None = None,
    force_download: bool = False,
    proxies: dict[str, str] | None = None,
    token: bool | str | None = None,
    revision: str | None = None,
    local_files_only: bool = False,
    **kwargs,
):
    """
    Loads the feature extractor configuration from a pretrained model feature extractor configuration.

    Args:
        pretrained_model_name_or_path (`str` or `os.PathLike`):
            This can be either:

            - a string, the *model id* of a pretrained model configuration hosted inside a model repo on
              huggingface.co.
            - a path to a *directory* containing a configuration file saved using the
              [`~FeatureExtractionMixin.save_pretrained`] method, e.g., `./my_model_directory/`.

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
        local_files_only (`bool`, *optional*, defaults to `False`):
            If `True`, will only try to load the feature extractor configuration from local files.

    <Tip>

    Passing `token=True` is required when you want to use a private model.

    </Tip>

    Returns:
        `Dict`: The configuration of the feature extractor.

    Examples:

    ```python
    # Download configuration from huggingface.co and cache.
    feature_extractor_config = get_feature_extractor_config("facebook/wav2vec2-base-960h")
    # This model does not have a feature extractor config so the result will be an empty dict.
    feature_extractor_config = get_feature_extractor_config("FacebookAI/xlm-roberta-base")

    # Save a pretrained feature extractor locally and you can reload its config
    from transformers import AutoFeatureExtractor

    feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-base-960h")
    feature_extractor.save_pretrained("feature-extractor-test")
    feature_extractor_config = get_feature_extractor_config("feature-extractor-test")
    ```"""
    # Load with a priority given to the nested processor config, if available in repo
    resolved_processor_file = cached_file(
        pretrained_model_name_or_path,
        filename=PROCESSOR_NAME,
        cache_dir=cache_dir,
        force_download=force_download,
        proxies=proxies,
        token=token,
        revision=revision,
        local_files_only=local_files_only,
        _raise_exceptions_for_gated_repo=False,
        _raise_exceptions_for_missing_entries=False,
    )
    resolved_feature_extractor_file = cached_file(
        pretrained_model_name_or_path,
        filename=FEATURE_EXTRACTOR_NAME,
        cache_dir=cache_dir,
        force_download=force_download,
        proxies=proxies,
        token=token,
        revision=revision,
        local_files_only=local_files_only,
        _raise_exceptions_for_gated_repo=False,
        _raise_exceptions_for_missing_entries=False,
    )

    # An empty list if none of the possible files is found in the repo
    if not resolved_feature_extractor_file and not resolved_processor_file:
        logger.info("Could not locate the feature extractor configuration file.")
        return {}

    # Load feature_extractor dict. Priority goes as (nested config if found -> feature extractor config)
    # We are downloading both configs because almost all models have a `processor_config.json` but
    # not all of these are nested. We need to check if it was saved recently as nested or if it is legacy style
    feature_extractor_dict = {}
    if resolved_processor_file is not None:
        processor_dict = safe_load_json_file(resolved_processor_file)
        if "feature_extractor" in processor_dict:
            feature_extractor_dict = processor_dict["feature_extractor"]

    if resolved_feature_extractor_file is not None and feature_extractor_dict is None:
        feature_extractor_dict = safe_load_json_file(resolved_feature_extractor_file)
    return feature_extractor_dict

