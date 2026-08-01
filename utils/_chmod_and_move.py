
def _chmod_and_move(src: Path, dst: Path) -> None:
    """Set correct permission before moving a blob from tmp directory to cache dir.

    Do not take into account the `umask` from the process as there is no convenient way
    to get it that is thread-safe.

    See:
    - About umask: https://docs.python.org/3/library/os.html#os.umask
    - Thread-safety: https://stackoverflow.com/a/70343066
    - About solution: https://github.com/huggingface/huggingface_hub/pull/1220#issuecomment-1326211591
    - Fix issue: https://github.com/huggingface/huggingface_hub/issues/1141
    - Fix issue: https://github.com/huggingface/huggingface_hub/issues/1215
    """
    # Get umask by creating a temporary file in the folder containing the incomplete file.
    # We know this folder is writable since the incomplete file has just been written there.
    # Probing next to `dst` is not always possible: when downloading to a local dir, `dst` is the
    # final file location and its parents might not be writable (e.g. read-only root filesystem).
    # See https://github.com/huggingface/huggingface_hub/issues/4304.
    tmp_file = src.parent / f"tmp_{uuid.uuid4()}"
    try:
        tmp_file.touch()
        cache_dir_mode = Path(tmp_file).stat().st_mode
        os.chmod(str(src), stat.S_IMODE(cache_dir_mode))
    except OSError as e:
        logger.warning(
            f"Could not set the permissions on the file '{src}'. Error: {e}.\nContinuing without setting permissions."
        )
    finally:
        try:
            tmp_file.unlink()
        except OSError:
            # fails if `tmp_file.touch()` failed => do nothing
            # See https://github.com/huggingface/huggingface_hub/issues/2359
            pass

    shutil.move(str(src), str(dst), copy_function=_copy_no_matter_what)

