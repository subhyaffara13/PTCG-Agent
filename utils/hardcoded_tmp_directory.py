
def hardcoded_tmp_directory(context, config):
    if config is not None and "tmp_dirs" in config:
        tmp_dirs = config["tmp_dirs"]
    else:
        tmp_dirs = ["/tmp", "/var/tmp", "/dev/shm"]  # nosec: B108

    if any(context.string_val.startswith(s) for s in tmp_dirs):
        return bandit.Issue(
            severity=bandit.MEDIUM,
            confidence=bandit.MEDIUM,
            cwe=issue.Cwe.INSECURE_TEMP_FILE,
            text="Probable insecure usage of temp file/directory.",
        )

