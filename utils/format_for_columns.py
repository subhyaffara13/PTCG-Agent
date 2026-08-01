
def format_for_columns(
    pkgs: _ProcessedDists, options: Values
) -> tuple[list[list[str]], list[str]]:
    """
    Convert the package data into something usable
    by output_package_listing_columns.
    """
    header = ["Package", "Version"]

    running_outdated = options.outdated
    if running_outdated:
        header.extend(["Latest", "Type"])

    def wheel_build_tag(dist: BaseDistribution) -> str | None:
        try:
            wheel_file = dist.read_text("WHEEL")
        except FileNotFoundError:
            return None
        return Parser().parsestr(wheel_file).get("Build")

    build_tags = [wheel_build_tag(p) for p in pkgs]
    has_build_tags = any(build_tags)
    if has_build_tags:
        header.append("Build")

    has_editables = any(x.editable for x in pkgs)
    if has_editables:
        header.append("Editable project location")

    if options.verbose >= 1:
        header.append("Location")
    if options.verbose >= 1:
        header.append("Installer")

    data = []
    for i, proj in enumerate(pkgs):
        # if we're working on the 'outdated' list, separate out the
        # latest_version and type
        row = [proj.raw_name, proj.raw_version]

        if running_outdated:
            row.append(str(proj.latest_version))
            row.append(proj.latest_filetype)

        if has_build_tags:
            row.append(build_tags[i] or "")

        if has_editables:
            row.append(proj.editable_project_location or "")

        if options.verbose >= 1:
            row.append(proj.location or "")
        if options.verbose >= 1:
            row.append(proj.installer)

        data.append(row)

    return data, header

