
def helper_for_dump_minify(contents: str) -> None:
    minified_repro_path = get_minifier_repro_path()
    log.warning("Writing minified repro to:\n%s", minified_repro_path)

    if use_buck:
        BuckTargetWriter(minified_repro_path).write()
    try:
        with open(minified_repro_path, "w") as fd:
            fd.write(contents)

    except OSError as e:
        log.exception("")
        raise NotImplementedError(f"Could not write to {minified_repro_path}") from e

