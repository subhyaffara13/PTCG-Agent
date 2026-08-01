
def cleanup_temp_dir() -> None:
    if tmp_dir is not None:
        tmp_dir.cleanup()

