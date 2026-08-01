
def section_key(line: str, config: Config) -> str:
    section = "B"

    if (
        not config.sort_relative_in_force_sorted_sections
        and config.reverse_relative
        and line.startswith("from .")
    ):
        match = re.match(r"^from (\.+)\s*(.*)", line)
        if match:  # pragma: no cover - regex always matches if line starts with "from ."
            line = f"from {' '.join(match.groups())}"
    if config.group_by_package and line.strip().startswith("from"):
        line = line.split(" import ", 1)[0]

    if config.lexicographical:
        line = _import_line_intro_re.sub("", _import_line_midline_import_re.sub(".", line))
    else:
        line = re.sub("^from ", "", line)
        line = re.sub("^import ", "", line)
    if config.sort_relative_in_force_sorted_sections:
        sep = " " if config.reverse_relative else "_"
        line = re.sub(r"^(\.+)", rf"\1{sep}", line)
    if line.split(" ")[0] in config.force_to_top:
        section = "A"
    # * If honor_case_in_force_sorted_sections is true, and case_sensitive and
    #   order_by_type are different, only ignore case in part of the line.
    # * Otherwise, let order_by_type decide the sorting of the whole line. This
    #   is only "correct" if case_sensitive and order_by_type have the same value.
    if config.honor_case_in_force_sorted_sections and config.case_sensitive != config.order_by_type:
        split_module = line.split(" import ", 1)
        if len(split_module) > 1:
            module_name, names = split_module
            if not config.case_sensitive:
                module_name = module_name.lower()
            if not config.order_by_type:
                names = names.lower()
            line = f"{module_name} import {names}"
        elif not config.case_sensitive:
            line = line.lower()
    elif not config.order_by_type:
        line = line.lower()

    return f"{section}{len(line) if config.length_sort else ''}{line}"

