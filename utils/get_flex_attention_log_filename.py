
def get_flex_attention_log_filename() -> str | None:
    flex_attention_file_name = os.environ.get(
        "TORCHINDUCTOR_FLEX_ATTENTION_LOGGING_FILE", None
    )
    if not flex_attention_file_name:
        return None

    return str(Path(flex_attention_file_name).with_suffix(".json"))

