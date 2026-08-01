
def core_metadata(dist) -> str:
    with io.StringIO() as buffer:
        dist.metadata.write_pkg_file(buffer)
        pkg_file_txt = buffer.getvalue()

    # Make sure core metadata is valid
    Metadata.from_email(pkg_file_txt, validate=True)  # can raise exceptions

    skip_prefixes: tuple[str, ...] = ()
    skip_lines = set()
    # ---- DIFF NORMALISATION ----
    # PEP 621 is very particular about author/maintainer metadata conversion, so skip
    skip_prefixes += ("Author:", "Author-email:", "Maintainer:", "Maintainer-email:")
    # May be redundant with Home-page
    skip_prefixes += ("Project-URL: Homepage,", "Home-page:")
    # May be missing in original (relying on default) but backfilled in the TOML
    skip_prefixes += ("Description-Content-Type:",)
    # Remove empty lines
    skip_lines.add("")

    result = []
    for line in pkg_file_txt.splitlines():
        if line.startswith(skip_prefixes) or line in skip_lines:
            continue
        result.append(line + "\n")

    return "".join(result)

