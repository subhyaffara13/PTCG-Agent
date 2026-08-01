
def get_expected_or_default(
    tested_configuration_file: str | Path,
    suffix: str,
    default: str,
) -> str:
    """Return the expected value from the file if it exists, or the given default."""
    expected = default
    path = Path(tested_configuration_file)
    expected_result_path = path.parent / f"{path.stem}.{suffix}"
    if expected_result_path.exists():
        with open(expected_result_path, encoding="utf8") as f:
            expected = f.read()
        # logging is helpful to realize your file is not taken into
        # account after a misspelling of the file name. The output of the
        # program is checked during the test so printing messes with the result.
        logging.info("%s exists.", expected_result_path)
    else:
        logging.info("%s not found, using '%s'.", expected_result_path, default)
    return expected

