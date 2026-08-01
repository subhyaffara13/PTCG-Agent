
def _test_cwd(
    current_working_directory: str | Path | None = None,
) -> Generator[None]:
    original_dir = os.getcwd()
    try:
        if current_working_directory is not None:
            os.chdir(current_working_directory)
        yield
    finally:
        os.chdir(original_dir)

