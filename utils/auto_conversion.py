
def auto_conversion(
    pretrained_model_name_or_path: str,
    ignore_errors_during_conversion: bool = False,
    safe_weights_name: str = "model.safetensors",
    safe_weights_index_name: str = "model.safetensors.index.json",
    **cached_file_kwargs,
):
    try:
        api = HfApi(token=cached_file_kwargs.get("token"), headers={"user-agent": http_user_agent()})
        sha = get_conversion_pr_reference(api, pretrained_model_name_or_path, **cached_file_kwargs)

        if sha is None:
            return None, None
        cached_file_kwargs["revision"] = sha
        del cached_file_kwargs["_commit_hash"]

        # This is an additional HEAD call that could be removed if we could infer sharded/non-sharded from the PR
        # description.
        sharded = api.file_exists(
            pretrained_model_name_or_path,
            safe_weights_index_name,
            revision=sha,
            token=cached_file_kwargs.get("token"),
        )
        filename = safe_weights_index_name if sharded else safe_weights_name

        resolved_archive_file = cached_file(pretrained_model_name_or_path, filename, **cached_file_kwargs)
        return resolved_archive_file, sha, sharded
    except Exception as e:
        if not ignore_errors_during_conversion:
            raise e

