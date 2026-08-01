
def get_expected_output(
    configuration_path: str | Path, user_specific_path: Path
) -> tuple[int, str]:
    """Get the expected output of a functional test."""
    exit_code = 0
    msg = (
        "we expect a single file of the form 'filename.32.out' where 'filename' represents "
        "the name of the configuration file, and '32' the expected error code."
    )
    possible_out_files = get_related_files(configuration_path, suffix_filter="out")
    if len(possible_out_files) > 1:
        logging.error(
            "Too much .out files for %s %s.",
            configuration_path,
            msg,
        )
        return -1, "out file is broken"
    if not possible_out_files:
        # logging is helpful to see what the expected exit code is and why.
        # The output of the program is checked during the test so printing
        # messes with the result.
        logging.info(".out file does not exists, so the expected exit code is 0")
        return 0, ""
    path = possible_out_files[0]
    try:
        exit_code = int(str(path.stem).rsplit(".", maxsplit=1)[-1])
    except Exception as e:  # pylint: disable=broad-except
        logging.error(
            "Wrong format for .out file name for %s %s: %s",
            configuration_path,
            msg,
            e,
        )
        return -1, "out file is broken"

    output = get_expected_or_default(
        configuration_path, suffix=f"{exit_code}.out", default=""
    )
    logging.info(
        "Output exists for %s so the expected exit code is %s",
        configuration_path,
        exit_code,
    )
    return exit_code, output.format(
        abspath=configuration_path,
        relpath=Path(configuration_path).relative_to(user_specific_path),
    )

