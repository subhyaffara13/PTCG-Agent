
def get_conv_log_filename() -> str | None:
    conv_file_name = os.environ.get("TORCHINDUCTOR_CONV_LOGGING_FILE", None)
    if not conv_file_name:
        return None

    return str(Path(conv_file_name).with_suffix(".json"))

