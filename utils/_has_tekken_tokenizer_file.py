
def _has_tekken_tokenizer_file(
    pretrained_model_name_or_path: str | os.PathLike[str],
    **kwargs,
) -> bool:
    subfolder = kwargs.get("subfolder", "")
    tekken_filename = os.path.join(subfolder, "tekken.json") if subfolder else "tekken.json"
    try:
        return has_file(
            pretrained_model_name_or_path,
            tekken_filename,
            revision=kwargs.get("revision"),
            token=kwargs.get("token"),
            cache_dir=kwargs.get("cache_dir"),
            local_files_only=kwargs.get("local_files_only", False),
        )
    except OSError:
        return False

