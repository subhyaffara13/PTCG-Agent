
def parse_mypy_comments(
    args: list[tuple[int, str]], template: Options
) -> tuple[dict[str, object], list[tuple[int, str]]]:
    """Parse a collection of inline mypy: configuration comments.

    Returns a dictionary of options to be applied and a list of error messages
    generated.
    """
    errors: list[tuple[int, str]] = []
    sections: dict[str, object] = {"enable_error_code": [], "disable_error_code": []}

    for lineno, line in args:
        # In order to easily match the behavior for bools, we abuse configparser.
        # Oddly, the only way to get the SectionProxy object with the getboolean
        # method is to create a config parser.
        parser = configparser.RawConfigParser()
        options, parse_errors = mypy_comments_to_config_map(line, template)
        if "python_version" in options:
            errors.append((lineno, "python_version not supported in inline configuration"))
            del options["python_version"]

        parser["dummy"] = options
        errors.extend((lineno, x) for x in parse_errors)

        stderr = StringIO()
        strict_found = False

        def set_strict_flags() -> None:
            nonlocal strict_found
            strict_found = True

        new_sections, reports = parse_section(
            "", template, set_strict_flags, parser["dummy"], ini_config_types, stderr=stderr
        )
        errors.extend((lineno, x) for x in stderr.getvalue().strip().split("\n") if x)
        if reports:
            errors.append((lineno, "Reports not supported in inline configuration"))
        if strict_found:
            errors.append(
                (
                    lineno,
                    'Setting "strict" not supported in inline configuration: specify it in '
                    "a configuration file instead, or set individual inline flags "
                    '(see "mypy -h" for the list of flags enabled in strict mode)',
                )
            )
        # Because this is currently special-cased
        # (the new_sections for an inline config *always* includes 'disable_error_code' and
        # 'enable_error_code' fields, usually empty, which overwrite the old ones),
        # we have to manipulate them specially.
        # This could use a refactor, but so could the whole subsystem.
        if (
            "enable_error_code" in new_sections
            and isinstance(neec := new_sections["enable_error_code"], list)
            and isinstance(eec := sections.get("enable_error_code", []), list)
        ):
            new_sections["enable_error_code"] = sorted(set(neec + eec))
        if (
            "disable_error_code" in new_sections
            and isinstance(ndec := new_sections["disable_error_code"], list)
            and isinstance(dec := sections.get("disable_error_code", []), list)
        ):
            new_sections["disable_error_code"] = sorted(set(ndec + dec))
        sections.update(new_sections)
    return sections, errors

